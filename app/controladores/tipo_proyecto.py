from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, extract
from typing import List, Optional
from datetime import datetime
import os
import shutil
from uuid import uuid4

from ..dependencias import get_db, get_current_user
from ..modelos import TipoProyecto as TipoProyectoModel, Proyecto, Estado, TipoEstado
from ..esquemas.tipo_proyecto import (
    TipoProyecto, TipoProyectoCreate, TipoProyectoUpdate, TipoProyectoEstadisticas
)
from ..esquemas.usuario import Usuario as UsuarioSchema
from ..config import settings

router = APIRouter(
    prefix="/tipos-proyecto",
    tags=["tipos-proyecto"]
)

# Directorio para almacenar documentos
UPLOAD_DIR = os.path.join(settings.UPLOAD_DIR, "tipos-proyecto")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/", response_model=List[TipoProyecto])
def read_tipos_proyecto(
    estado_id: Optional[int] = None,
    tipo_estado_id: Optional[int] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Obtener lista de tipos de proyecto con filtros opcionales.
    Solo administradores pueden ver todos los tipos.
    Los usuarios normales solo ven tipos activos.
    """
    query = db.query(TipoProyectoModel)

    # Aplicar filtros
    if estado_id:
        query = query.filter(TipoProyectoModel.estado_id == estado_id)
    if tipo_estado_id:
        query = query.filter(TipoProyectoModel.tipo_estado_id == tipo_estado_id)
    if search:
        search_filter = or_(
            TipoProyectoModel.nombre.ilike(f"%{search}%"),
            TipoProyectoModel.descripcion.ilike(f"%{search}%"),
            TipoProyectoModel.codigo.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)

    # Restricción para usuarios normales
    if current_user.rol != "Admin":
        query = query.filter(TipoProyectoModel.estado_id == 1)  # Solo activos

    tipos = query.offset(skip).limit(limit).all()
    return tipos

@router.get("/{tipo_id}", response_model=TipoProyecto)
def read_tipo_proyecto(
    tipo_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Obtener un tipo de proyecto específico por ID.
    Solo administradores pueden ver tipos inactivos.
    """
    tipo = db.query(TipoProyectoModel).filter(TipoProyectoModel.id == tipo_id).first()
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de proyecto no encontrado")

    # Verificar permisos
    if current_user.rol != "Admin" and tipo.estado_id != 1:
        raise HTTPException(status_code=403, detail="No tiene permiso para ver este tipo de proyecto")

    return tipo

@router.post("/", response_model=TipoProyecto)
def create_tipo_proyecto(
    tipo: TipoProyectoCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Crear un nuevo tipo de proyecto.
    Solo administradores pueden crear tipos de proyecto.
    """
    if current_user.rol != "Admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden crear tipos de proyecto")

    # Verificar que el estado existe
    estado = db.query(Estado).filter(Estado.id == tipo.estado_id).first()
    if not estado:
        raise HTTPException(status_code=404, detail="Estado no encontrado")

    # Verificar que el tipo de estado existe
    tipo_estado = db.query(TipoEstado).filter(TipoEstado.id == tipo.tipo_estado_id).first()
    if not tipo_estado:
        raise HTTPException(status_code=404, detail="Tipo de estado no encontrado")

    # Verificar que el código es único
    if db.query(TipoProyectoModel).filter(TipoProyectoModel.codigo == tipo.codigo).first():
        raise HTTPException(status_code=400, detail="El código ya está en uso")

    db_tipo = TipoProyectoModel(**tipo.dict())
    db.add(db_tipo)
    db.commit()
    db.refresh(db_tipo)
    return db_tipo

@router.put("/{tipo_id}", response_model=TipoProyecto)
def update_tipo_proyecto(
    tipo_id: int,
    tipo: TipoProyectoUpdate,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Actualizar un tipo de proyecto existente.
    Solo administradores pueden actualizar tipos de proyecto.
    """
    if current_user.rol != "Admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden actualizar tipos de proyecto")

    db_tipo = db.query(TipoProyectoModel).filter(TipoProyectoModel.id == tipo_id).first()
    if not db_tipo:
        raise HTTPException(status_code=404, detail="Tipo de proyecto no encontrado")

    # Verificar que el estado existe si se proporciona
    if tipo.estado_id:
        estado = db.query(Estado).filter(Estado.id == tipo.estado_id).first()
        if not estado:
            raise HTTPException(status_code=404, detail="Estado no encontrado")

    # Verificar que el tipo de estado existe si se proporciona
    if tipo.tipo_estado_id:
        tipo_estado = db.query(TipoEstado).filter(TipoEstado.id == tipo.tipo_estado_id).first()
        if not tipo_estado:
            raise HTTPException(status_code=404, detail="Tipo de estado no encontrado")

    # Verificar que el código es único si se proporciona
    if tipo.codigo and tipo.codigo != db_tipo.codigo:
        if db.query(TipoProyectoModel).filter(TipoProyectoModel.codigo == tipo.codigo).first():
            raise HTTPException(status_code=400, detail="El código ya está en uso")

    # Actualizar campos
    for key, value in tipo.dict(exclude_unset=True).items():
        setattr(db_tipo, key, value)

    db_tipo.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_tipo)
    return db_tipo

@router.delete("/{tipo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tipo_proyecto(
    tipo_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Eliminar un tipo de proyecto.
    Solo administradores pueden eliminar tipos de proyecto.
    Se verifica que no haya proyectos asociados.
    """
    if current_user.rol != "Admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden eliminar tipos de proyecto")

    tipo = db.query(TipoProyectoModel).filter(TipoProyectoModel.id == tipo_id).first()
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de proyecto no encontrado")

    # Verificar si hay proyectos asociados
    if db.query(Proyecto).filter(Proyecto.tipo_id == tipo_id).first():
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar el tipo de proyecto porque tiene proyectos asociados"
        )

    # Eliminar documentos asociados
    if tipo.documentos:
        for doc in tipo.documentos:
            doc_path = os.path.join(UPLOAD_DIR, doc)
            if os.path.exists(doc_path):
                os.remove(doc_path)

    db.delete(tipo)
    db.commit()

@router.post("/{tipo_id}/documentos")
def upload_documento(
    tipo_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Subir un documento para un tipo de proyecto.
    Solo administradores pueden subir documentos.
    """
    if current_user.rol != "Admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden subir documentos")

    tipo = db.query(TipoProyectoModel).filter(TipoProyectoModel.id == tipo_id).first()
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de proyecto no encontrado")

    # Generar nombre único para el archivo
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    # Guardar archivo
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Actualizar lista de documentos
    if not tipo.documentos:
        tipo.documentos = []
    tipo.documentos.append(unique_filename)
    tipo.fecha_actualizacion = datetime.utcnow()
    db.commit()

    return {"filename": unique_filename}

@router.get("/estadisticas/", response_model=TipoProyectoEstadisticas)
def get_estadisticas(
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Obtener estadísticas de tipos de proyecto.
    Solo administradores pueden ver estadísticas.
    """
    if current_user.rol != "Admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden ver estadísticas")

    # Total de tipos
    total_tipos = db.query(TipoProyectoModel).count()

    # Tipos por estado
    tipos_por_estado = db.query(
        Estado.nombre,
        func.count(TipoProyectoModel.id)
    ).join(TipoProyectoModel).group_by(Estado.nombre).all()
    tipos_por_estado = dict(tipos_por_estado)

    # Tipos por tipo de estado
    tipos_por_tipo_estado = db.query(
        TipoEstado.nombre,
        func.count(TipoProyectoModel.id)
    ).join(TipoProyectoModel).group_by(TipoEstado.nombre).all()
    tipos_por_tipo_estado = dict(tipos_por_tipo_estado)

    # Total de proyectos
    total_proyectos = db.query(Proyecto).count()

    # Proyectos por tipo
    proyectos_por_tipo = db.query(
        TipoProyectoModel.nombre,
        func.count(Proyecto.id)
    ).join(Proyecto).group_by(TipoProyectoModel.nombre).all()
    proyectos_por_tipo = dict(proyectos_por_tipo)

    # Promedio de proyectos por tipo
    promedio_proyectos = total_proyectos / total_tipos if total_tipos > 0 else 0

    return TipoProyectoEstadisticas(
        total_tipos=total_tipos,
        tipos_por_estado=tipos_por_estado,
        tipos_por_tipo_estado=tipos_por_tipo_estado,
        total_proyectos=total_proyectos,
        proyectos_por_tipo=proyectos_por_tipo,
        promedio_proyectos_por_tipo=promedio_proyectos
    )
