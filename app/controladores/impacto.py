from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, extract
from typing import List, Optional
from datetime import datetime, timedelta
import os
import json
from uuid import uuid4

from ..dependencias import get_db, get_current_user
from ..modelos import Impacto as ImpactoModel, Usuario, Extension
from ..esquemas.impacto import (
    Impacto, ImpactoCreate, ImpactoUpdate, ImpactoEstadisticas,
    TipoImpacto, NivelImpacto
)
from ..esquemas.usuario import Usuario as UsuarioSchema
from ..config import settings

router = APIRouter(
    prefix="/impactos",
    tags=["impactos"]
)

# Directorio para almacenar documentos
DOCS_DIR = os.path.join(settings.UPLOAD_DIR, "impactos")
os.makedirs(DOCS_DIR, exist_ok=True)

@router.get("/", response_model=List[Impacto])
def read_impactos(
    tipo: Optional[TipoImpacto] = None,
    nivel: Optional[NivelImpacto] = None,
    extension_id: Optional[int] = None,
    usuario_id: Optional[int] = None,
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Obtener lista de impactos con filtros opcionales.
    Los usuarios solo ven los impactos de sus extensiones.
    Los administradores pueden ver todos los impactos.
    """
    query = db.query(ImpactoModel)

    # Aplicar filtros
    if tipo:
        query = query.filter(ImpactoModel.tipo == tipo)
    if nivel:
        query = query.filter(ImpactoModel.nivel == nivel)
    if extension_id:
        query = query.filter(ImpactoModel.extension_id == extension_id)
    if usuario_id:
        query = query.filter(ImpactoModel.usuario_id == usuario_id)
    if fecha_inicio:
        query = query.filter(ImpactoModel.fecha_impacto >= fecha_inicio)
    if fecha_fin:
        query = query.filter(ImpactoModel.fecha_impacto <= fecha_fin)
    if search:
        search_filter = or_(
            ImpactoModel.titulo.ilike(f"%{search}%"),
            ImpactoModel.descripcion.ilike(f"%{search}%"),
            ImpactoModel.resultados.ilike(f"%{search}%")
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
            
        query = query.filter(ImpactoModel.extension_id.in_(extensiones_ids))

    # Ordenar por fecha de impacto descendente
    query = query.order_by(ImpactoModel.fecha_impacto.desc())

    impactos = query.offset(skip).limit(limit).all()
    return impactos

@router.get("/{impacto_id}", response_model=Impacto)
def read_impacto(
    impacto_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Obtener un impacto específico por ID.
    Los usuarios solo pueden ver los impactos de sus extensiones.
    Los administradores pueden ver cualquier impacto.
    """
    impacto = db.query(ImpactoModel).filter(ImpactoModel.id == impacto_id).first()
    if not impacto:
        raise HTTPException(status_code=404, detail="Impacto no encontrado")

    # Verificar permisos
    if current_user.rol != "Admin":
        extension = db.query(Extension).filter(Extension.id == impacto.extension_id).first()
        if not extension or extension.usuario_id != current_user.id:
            raise HTTPException(status_code=403, detail="No tiene permiso para ver este impacto")

    return impacto

@router.post("/", response_model=Impacto)
def create_impacto(
    impacto: ImpactoCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Crear un nuevo impacto.
    Los usuarios solo pueden crear impactos para sus extensiones.
    """
    # Verificar que la extensión existe
    extension = db.query(Extension).filter(Extension.id == impacto.extension_id).first()
    if not extension:
        raise HTTPException(status_code=404, detail="Extensión no encontrada")

    # Verificar permisos
    if current_user.rol != "Admin" and extension.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tiene permiso para crear impactos para esta extensión")

    # Verificar que el usuario existe
    usuario = db.query(Usuario).filter(Usuario.id == impacto.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db_impacto = ImpactoModel(**impacto.dict())
    db.add(db_impacto)
    db.commit()
    db.refresh(db_impacto)
    return db_impacto

@router.put("/{impacto_id}", response_model=Impacto)
def update_impacto(
    impacto_id: int,
    impacto: ImpactoUpdate,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Actualizar un impacto existente.
    Los usuarios solo pueden actualizar los impactos de sus extensiones.
    Los administradores pueden actualizar cualquier impacto.
    """
    db_impacto = db.query(ImpactoModel).filter(ImpactoModel.id == impacto_id).first()
    if not db_impacto:
        raise HTTPException(status_code=404, detail="Impacto no encontrado")

    # Verificar permisos
    if current_user.rol != "Admin":
        extension = db.query(Extension).filter(Extension.id == db_impacto.extension_id).first()
        if not extension or extension.usuario_id != current_user.id:
            raise HTTPException(status_code=403, detail="No tiene permiso para actualizar este impacto")

    # Actualizar campos
    for key, value in impacto.dict(exclude_unset=True).items():
        setattr(db_impacto, key, value)

    db_impacto.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_impacto)
    return db_impacto

@router.delete("/{impacto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_impacto(
    impacto_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Eliminar un impacto.
    Los usuarios solo pueden eliminar los impactos de sus extensiones.
    Los administradores pueden eliminar cualquier impacto.
    """
    impacto = db.query(ImpactoModel).filter(ImpactoModel.id == impacto_id).first()
    if not impacto:
        raise HTTPException(status_code=404, detail="Impacto no encontrado")

    # Verificar permisos
    if current_user.rol != "Admin":
        extension = db.query(Extension).filter(Extension.id == impacto.extension_id).first()
        if not extension or extension.usuario_id != current_user.id:
            raise HTTPException(status_code=403, detail="No tiene permiso para eliminar este impacto")

    # Eliminar documentos si existen
    if impacto.documentos:
        for doc in impacto.documentos:
            file_path = os.path.join(DOCS_DIR, os.path.basename(doc))
            if os.path.exists(file_path):
                os.remove(file_path)

    db.delete(impacto)
    db.commit()

@router.post("/{impacto_id}/documentos")
async def upload_documento(
    impacto_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Subir un documento para un impacto.
    Los usuarios solo pueden subir documentos para los impactos de sus extensiones.
    Los administradores pueden subir documentos para cualquier impacto.
    """
    impacto = db.query(ImpactoModel).filter(ImpactoModel.id == impacto_id).first()
    if not impacto:
        raise HTTPException(status_code=404, detail="Impacto no encontrado")

    # Verificar permisos
    if current_user.rol != "Admin":
        extension = db.query(Extension).filter(Extension.id == impacto.extension_id).first()
        if not extension or extension.usuario_id != current_user.id:
            raise HTTPException(status_code=403, detail="No tiene permiso para subir documentos para este impacto")

    # Generar nombre único para el archivo
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid4()}{file_extension}"
    file_path = os.path.join(DOCS_DIR, unique_filename)

    # Guardar archivo
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Actualizar lista de documentos
    if not impacto.documentos:
        impacto.documentos = []
    impacto.documentos.append(f"/impactos/{unique_filename}")
    impacto.fecha_actualizacion = datetime.utcnow()
    db.commit()

    return {"filename": unique_filename}

@router.get("/estadisticas/", response_model=ImpactoEstadisticas)
def get_estadisticas(
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Obtener estadísticas de impactos.
    Solo administradores pueden ver estadísticas globales.
    Los usuarios normales solo ven estadísticas de sus extensiones.
    """
    # Base query
    query = db.query(ImpactoModel)

    # Filtrar por usuario si no es admin
    if current_user.rol != "Admin":
        extensiones_usuario = db.query(Extension.id).filter(
            Extension.usuario_id == current_user.id
        ).all()
        extensiones_ids = [e.id for e in extensiones_usuario]
        
        if not extensiones_ids:
            return ImpactoEstadisticas(
                total_impactos=0,
                impactos_por_tipo={},
                impactos_por_nivel={},
                impactos_por_extension={},
                impactos_por_usuario={},
                total_beneficiarios_directos=0,
                total_beneficiarios_indirectos=0,
                promedio_beneficiarios=0,
                impactos_ultimo_mes=0,
                impactos_por_sostenibilidad={},
                impactos_por_replicabilidad={}
            )
            
        query = query.filter(ImpactoModel.extension_id.in_(extensiones_ids))

    # Total de impactos
    total_impactos = query.count()

    # Impactos por tipo
    impactos_por_tipo = query.with_entities(
        ImpactoModel.tipo,
        func.count(ImpactoModel.id)
    ).group_by(ImpactoModel.tipo).all()
    impactos_por_tipo = dict(impactos_por_tipo)

    # Impactos por nivel
    impactos_por_nivel = query.with_entities(
        ImpactoModel.nivel,
        func.count(ImpactoModel.id)
    ).group_by(ImpactoModel.nivel).all()
    impactos_por_nivel = dict(impactos_por_nivel)

    # Impactos por extensión
    impactos_por_extension = query.join(Extension).with_entities(
        Extension.nombre,
        func.count(ImpactoModel.id)
    ).group_by(Extension.nombre).all()
    impactos_por_extension = dict(impactos_por_extension)

    # Impactos por usuario
    impactos_por_usuario = query.join(Usuario).with_entities(
        Usuario.nombre,
        func.count(ImpactoModel.id)
    ).group_by(Usuario.nombre).all()
    impactos_por_usuario = dict(impactos_por_usuario)

    # Totales de beneficiarios
    total_beneficiarios_directos = query.with_entities(
        func.sum(ImpactoModel.beneficiarios_directos)
    ).scalar() or 0

    total_beneficiarios_indirectos = query.with_entities(
        func.sum(ImpactoModel.beneficiarios_indirectos)
    ).scalar() or 0

    # Promedio de beneficiarios
    impactos_con_beneficiarios = query.filter(
        ImpactoModel.beneficiarios_directos != None,
        ImpactoModel.beneficiarios_indirectos != None
    ).all()
    
    if impactos_con_beneficiarios:
        promedio_beneficiarios = sum(
            (i.beneficiarios_directos or 0) + (i.beneficiarios_indirectos or 0)
            for i in impactos_con_beneficiarios
        ) / len(impactos_con_beneficiarios)
    else:
        promedio_beneficiarios = 0

    # Impactos del último mes
    un_mes_atras = datetime.utcnow() - timedelta(days=30)
    impactos_ultimo_mes = query.filter(ImpactoModel.fecha_creacion >= un_mes_atras).count()

    # Impactos por sostenibilidad
    impactos_por_sostenibilidad = query.with_entities(
        ImpactoModel.sostenibilidad,
        func.count(ImpactoModel.id)
    ).group_by(ImpactoModel.sostenibilidad).all()
    impactos_por_sostenibilidad = dict(impactos_por_sostenibilidad)

    # Impactos por replicabilidad
    impactos_por_replicabilidad = query.with_entities(
        ImpactoModel.replicabilidad,
        func.count(ImpactoModel.id)
    ).group_by(ImpactoModel.replicabilidad).all()
    impactos_por_replicabilidad = dict(impactos_por_replicabilidad)

    return ImpactoEstadisticas(
        total_impactos=total_impactos,
        impactos_por_tipo=impactos_por_tipo,
        impactos_por_nivel=impactos_por_nivel,
        impactos_por_extension=impactos_por_extension,
        impactos_por_usuario=impactos_por_usuario,
        total_beneficiarios_directos=total_beneficiarios_directos,
        total_beneficiarios_indirectos=total_beneficiarios_indirectos,
        promedio_beneficiarios=promedio_beneficiarios,
        impactos_ultimo_mes=impactos_ultimo_mes,
        impactos_por_sostenibilidad=impactos_por_sostenibilidad,
        impactos_por_replicabilidad=impactos_por_replicabilidad
    )
