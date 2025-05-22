from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, extract
from typing import List, Optional
from datetime import datetime, timedelta
import os
import json
from uuid import uuid4

from ..dependencias import get_db, get_current_user
from ..modelos import Seguimiento as SeguimientoModel, Usuario, Extension
from ..esquemas.seguimiento import (
    Seguimiento, SeguimientoCreate, SeguimientoUpdate, SeguimientoEstadisticas,
    TipoSeguimiento, EstadoSeguimiento
)
from ..esquemas.usuario import Usuario as UsuarioSchema
from ..config import settings

router = APIRouter(
    prefix="/seguimientos",
    tags=["seguimientos"]
)

# Directorio para almacenar documentos
DOCS_DIR = os.path.join(settings.UPLOAD_DIR, "seguimientos")
os.makedirs(DOCS_DIR, exist_ok=True)

@router.get("/", response_model=List[Seguimiento])
def read_seguimientos(
    tipo: Optional[TipoSeguimiento] = None,
    estado: Optional[EstadoSeguimiento] = None,
    extension_id: Optional[int] = None,
    usuario_id: Optional[int] = None,
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
    prioridad: Optional[int] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Obtener lista de seguimientos con filtros opcionales.
    Los usuarios solo ven los seguimientos de sus extensiones.
    Los administradores pueden ver todos los seguimientos.
    """
    query = db.query(SeguimientoModel)

    # Aplicar filtros
    if tipo:
        query = query.filter(SeguimientoModel.tipo == tipo)
    if estado:
        query = query.filter(SeguimientoModel.estado == estado)
    if extension_id:
        query = query.filter(SeguimientoModel.extension_id == extension_id)
    if usuario_id:
        query = query.filter(SeguimientoModel.usuario_id == usuario_id)
    if fecha_inicio:
        query = query.filter(SeguimientoModel.fecha_creacion >= fecha_inicio)
    if fecha_fin:
        query = query.filter(SeguimientoModel.fecha_creacion <= fecha_fin)
    if prioridad:
        query = query.filter(SeguimientoModel.prioridad == prioridad)
    if search:
        search_filter = or_(
            SeguimientoModel.titulo.ilike(f"%{search}%"),
            SeguimientoModel.descripcion.ilike(f"%{search}%"),
            SeguimientoModel.observaciones.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)

    # Restricción por usuario si no es administrador
    if current_user.rol != "Admin":
        # Obtener extensiones del usuario
        extensiones_usuario = db.query(Extension.id).filter(
            Extension.usuario_id == current_user.id
        ).all()
        extensiones_ids = [e.id for e in extensiones_usuario]
        
        if not extensiones_ids:
            return []
            
        query = query.filter(SeguimientoModel.extension_id.in_(extensiones_ids))

    # Ordenar por fecha de creación descendente
    query = query.order_by(SeguimientoModel.fecha_creacion.desc())

    seguimientos = query.offset(skip).limit(limit).all()
    return seguimientos

@router.get("/{seguimiento_id}", response_model=Seguimiento)
def read_seguimiento(
    seguimiento_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Obtener un seguimiento específico por ID.
    Los usuarios solo pueden ver los seguimientos de sus extensiones.
    Los administradores pueden ver cualquier seguimiento.
    """
    seguimiento = db.query(SeguimientoModel).filter(SeguimientoModel.id == seguimiento_id).first()
    if not seguimiento:
        raise HTTPException(status_code=404, detail="Seguimiento no encontrado")

    # Verificar permisos
    if current_user.rol != "Admin":
        extension = db.query(Extension).filter(Extension.id == seguimiento.extension_id).first()
        if not extension or extension.usuario_id != current_user.id:
            raise HTTPException(status_code=403, detail="No tiene permiso para ver este seguimiento")

    return seguimiento

@router.post("/", response_model=Seguimiento)
def create_seguimiento(
    seguimiento: SeguimientoCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Crear un nuevo seguimiento.
    Los usuarios solo pueden crear seguimientos para sus extensiones.
    """
    # Verificar que la extensión existe
    extension = db.query(Extension).filter(Extension.id == seguimiento.extension_id).first()
    if not extension:
        raise HTTPException(status_code=404, detail="Extensión no encontrada")

    # Verificar permisos
    if current_user.rol != "Admin" and extension.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tiene permiso para crear seguimientos para esta extensión")

    # Verificar que el usuario existe
    usuario = db.query(Usuario).filter(Usuario.id == seguimiento.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db_seguimiento = SeguimientoModel(**seguimiento.dict())
    db.add(db_seguimiento)
    db.commit()
    db.refresh(db_seguimiento)
    return db_seguimiento

@router.put("/{seguimiento_id}", response_model=Seguimiento)
def update_seguimiento(
    seguimiento_id: int,
    seguimiento: SeguimientoUpdate,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Actualizar un seguimiento existente.
    Los usuarios solo pueden actualizar los seguimientos de sus extensiones.
    Los administradores pueden actualizar cualquier seguimiento.
    """
    db_seguimiento = db.query(SeguimientoModel).filter(SeguimientoModel.id == seguimiento_id).first()
    if not db_seguimiento:
        raise HTTPException(status_code=404, detail="Seguimiento no encontrado")

    # Verificar permisos
    if current_user.rol != "Admin":
        extension = db.query(Extension).filter(Extension.id == db_seguimiento.extension_id).first()
        if not extension or extension.usuario_id != current_user.id:
            raise HTTPException(status_code=403, detail="No tiene permiso para actualizar este seguimiento")

    # Actualizar campos
    for key, value in seguimiento.dict(exclude_unset=True).items():
        setattr(db_seguimiento, key, value)

    db_seguimiento.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_seguimiento)
    return db_seguimiento

@router.delete("/{seguimiento_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_seguimiento(
    seguimiento_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Eliminar un seguimiento.
    Los usuarios solo pueden eliminar los seguimientos de sus extensiones.
    Los administradores pueden eliminar cualquier seguimiento.
    """
    seguimiento = db.query(SeguimientoModel).filter(SeguimientoModel.id == seguimiento_id).first()
    if not seguimiento:
        raise HTTPException(status_code=404, detail="Seguimiento no encontrado")

    # Verificar permisos
    if current_user.rol != "Admin":
        extension = db.query(Extension).filter(Extension.id == seguimiento.extension_id).first()
        if not extension or extension.usuario_id != current_user.id:
            raise HTTPException(status_code=403, detail="No tiene permiso para eliminar este seguimiento")

    # Eliminar documentos si existen
    if seguimiento.documentos:
        for doc in seguimiento.documentos:
            file_path = os.path.join(DOCS_DIR, os.path.basename(doc))
            if os.path.exists(file_path):
                os.remove(file_path)

    db.delete(seguimiento)
    db.commit()

@router.post("/{seguimiento_id}/documentos")
async def upload_documento(
    seguimiento_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Subir un documento para un seguimiento.
    Los usuarios solo pueden subir documentos para los seguimientos de sus extensiones.
    Los administradores pueden subir documentos para cualquier seguimiento.
    """
    seguimiento = db.query(SeguimientoModel).filter(SeguimientoModel.id == seguimiento_id).first()
    if not seguimiento:
        raise HTTPException(status_code=404, detail="Seguimiento no encontrado")

    # Verificar permisos
    if current_user.rol != "Admin":
        extension = db.query(Extension).filter(Extension.id == seguimiento.extension_id).first()
        if not extension or extension.usuario_id != current_user.id:
            raise HTTPException(status_code=403, detail="No tiene permiso para subir documentos para este seguimiento")

    # Generar nombre único para el archivo
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid4()}{file_extension}"
    file_path = os.path.join(DOCS_DIR, unique_filename)

    # Guardar archivo
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Actualizar lista de documentos
    if not seguimiento.documentos:
        seguimiento.documentos = []
    seguimiento.documentos.append(f"/seguimientos/{unique_filename}")
    seguimiento.fecha_actualizacion = datetime.utcnow()
    db.commit()

    return {"filename": unique_filename}

@router.get("/estadisticas/", response_model=SeguimientoEstadisticas)
def get_estadisticas(
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Obtener estadísticas de seguimientos.
    Solo administradores pueden ver estadísticas globales.
    Los usuarios normales solo ven estadísticas de sus extensiones.
    """
    # Base query
    query = db.query(SeguimientoModel)

    # Filtrar por usuario si no es admin
    if current_user.rol != "Admin":
        extensiones_usuario = db.query(Extension.id).filter(
            Extension.usuario_id == current_user.id
        ).all()
        extensiones_ids = [e.id for e in extensiones_usuario]
        
        if not extensiones_ids:
            return SeguimientoEstadisticas(
                total_seguimientos=0,
                seguimientos_por_tipo={},
                seguimientos_por_estado={},
                seguimientos_por_extension={},
                seguimientos_por_usuario={},
                seguimientos_pendientes=0,
                seguimientos_en_proceso=0,
                seguimientos_completados=0,
                seguimientos_retrasados=0,
                seguimientos_cancelados=0,
                promedio_avance=0,
                seguimientos_ultimo_mes=0,
                seguimientos_por_prioridad={},
                seguimientos_por_impacto={}
            )
            
        query = query.filter(SeguimientoModel.extension_id.in_(extensiones_ids))

    # Total de seguimientos
    total_seguimientos = query.count()

    # Seguimientos por tipo
    seguimientos_por_tipo = query.with_entities(
        SeguimientoModel.tipo,
        func.count(SeguimientoModel.id)
    ).group_by(SeguimientoModel.tipo).all()
    seguimientos_por_tipo = dict(seguimientos_por_tipo)

    # Seguimientos por estado
    seguimientos_por_estado = query.with_entities(
        SeguimientoModel.estado,
        func.count(SeguimientoModel.id)
    ).group_by(SeguimientoModel.estado).all()
    seguimientos_por_estado = dict(seguimientos_por_estado)

    # Seguimientos por extensión
    seguimientos_por_extension = query.join(Extension).with_entities(
        Extension.nombre,
        func.count(SeguimientoModel.id)
    ).group_by(Extension.nombre).all()
    seguimientos_por_extension = dict(seguimientos_por_extension)

    # Seguimientos por usuario
    seguimientos_por_usuario = query.join(Usuario).with_entities(
        Usuario.nombre,
        func.count(SeguimientoModel.id)
    ).group_by(Usuario.nombre).all()
    seguimientos_por_usuario = dict(seguimientos_por_usuario)

    # Seguimientos por estado específico
    seguimientos_pendientes = query.filter(SeguimientoModel.estado == EstadoSeguimiento.PENDIENTE).count()
    seguimientos_en_proceso = query.filter(SeguimientoModel.estado == EstadoSeguimiento.EN_PROCESO).count()
    seguimientos_completados = query.filter(SeguimientoModel.estado == EstadoSeguimiento.COMPLETADO).count()
    seguimientos_retrasados = query.filter(SeguimientoModel.estado == EstadoSeguimiento.RETRASADO).count()
    seguimientos_cancelados = query.filter(SeguimientoModel.estado == EstadoSeguimiento.CANCELADO).count()

    # Promedio de avance
    seguimientos_con_avance = query.filter(SeguimientoModel.porcentaje_avance != None).all()
    if seguimientos_con_avance:
        promedio_avance = sum(s.porcentaje_avance for s in seguimientos_con_avance) / len(seguimientos_con_avance)
    else:
        promedio_avance = 0

    # Seguimientos del último mes
    un_mes_atras = datetime.utcnow() - timedelta(days=30)
    seguimientos_ultimo_mes = query.filter(SeguimientoModel.fecha_creacion >= un_mes_atras).count()

    # Seguimientos por prioridad
    seguimientos_por_prioridad = query.with_entities(
        SeguimientoModel.prioridad,
        func.count(SeguimientoModel.id)
    ).group_by(SeguimientoModel.prioridad).all()
    seguimientos_por_prioridad = dict(seguimientos_por_prioridad)

    # Seguimientos por impacto
    seguimientos_por_impacto = query.with_entities(
        SeguimientoModel.impacto,
        func.count(SeguimientoModel.id)
    ).group_by(SeguimientoModel.impacto).all()
    seguimientos_por_impacto = dict(seguimientos_por_impacto)

    return SeguimientoEstadisticas(
        total_seguimientos=total_seguimientos,
        seguimientos_por_tipo=seguimientos_por_tipo,
        seguimientos_por_estado=seguimientos_por_estado,
        seguimientos_por_extension=seguimientos_por_extension,
        seguimientos_por_usuario=seguimientos_por_usuario,
        seguimientos_pendientes=seguimientos_pendientes,
        seguimientos_en_proceso=seguimientos_en_proceso,
        seguimientos_completados=seguimientos_completados,
        seguimientos_retrasados=seguimientos_retrasados,
        seguimientos_cancelados=seguimientos_cancelados,
        promedio_avance=promedio_avance,
        seguimientos_ultimo_mes=seguimientos_ultimo_mes,
        seguimientos_por_prioridad=seguimientos_por_prioridad,
        seguimientos_por_impacto=seguimientos_por_impacto
    )
