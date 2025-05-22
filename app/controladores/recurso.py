from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, extract
from typing import List, Optional
from datetime import datetime
import os
import shutil
from uuid import uuid4

from ..dependencias import get_db, get_current_user
from ..modelos import Recurso as RecursoModel, Usuario, Estado, TipoEstado, Extension, Programa, Facultad
from ..esquemas.recurso import Recurso, RecursoCreate, RecursoUpdate, RecursoEstadisticas
from ..esquemas.usuario import Usuario as UsuarioSchema
from ..config import settings

router = APIRouter(
    prefix="/recursos",
    tags=["recursos"]
)

# Configuración del directorio de documentos
UPLOAD_DIR = os.path.join(settings.UPLOAD_DIR, "recursos")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/", response_model=List[Recurso])
def read_recursos(
    tipo: Optional[str] = None,
    estado_id: Optional[int] = None,
    responsable_id: Optional[int] = None,
    facultad_id: Optional[int] = None,
    programa_id: Optional[int] = None,
    extension_id: Optional[int] = None,
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Obtener lista de recursos con filtros opcionales.
    Solo administradores pueden ver todos los recursos.
    Los usuarios normales solo ven los recursos de su facultad.
    """
    query = db.query(RecursoModel)

    # Aplicar filtros
    if tipo:
        query = query.filter(RecursoModel.tipo == tipo)
    if estado_id:
        query = query.filter(RecursoModel.estado_id == estado_id)
    if responsable_id:
        query = query.filter(RecursoModel.responsable_id == responsable_id)
    if facultad_id:
        query = query.filter(RecursoModel.facultad_id == facultad_id)
    if programa_id:
        query = query.filter(RecursoModel.programa_id == programa_id)
    if extension_id:
        query = query.filter(RecursoModel.extension_id == extension_id)
    if fecha_inicio:
        query = query.filter(RecursoModel.fecha_creacion >= fecha_inicio)
    if fecha_fin:
        query = query.filter(RecursoModel.fecha_creacion <= fecha_fin)
    if search:
        search_filter = or_(
            RecursoModel.nombre.ilike(f"%{search}%"),
            RecursoModel.descripcion.ilike(f"%{search}%"),
            RecursoModel.codigo.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)

    # Restricción por facultad para usuarios no administradores
    if current_user.rol != "Admin":
        query = query.filter(RecursoModel.facultad_id == current_user.facultad_id)

    recursos = query.offset(skip).limit(limit).all()
    return recursos

@router.get("/{recurso_id}", response_model=Recurso)
def read_recurso(
    recurso_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Obtener un recurso específico por ID.
    Solo administradores pueden ver cualquier recurso.
    Los usuarios normales solo pueden ver recursos de su facultad.
    """
    recurso = db.query(RecursoModel).filter(RecursoModel.id == recurso_id).first()
    if not recurso:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")

    # Verificar permisos
    if current_user.rol != "Admin" and recurso.facultad_id != current_user.facultad_id:
        raise HTTPException(status_code=403, detail="No tiene permiso para ver este recurso")

    return recurso

@router.post("/", response_model=Recurso)
def create_recurso(
    recurso: RecursoCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Crear un nuevo recurso.
    Solo administradores pueden crear recursos.
    """
    if current_user.rol != "Admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden crear recursos")

    # Verificar que la facultad existe
    facultad = db.query(Facultad).filter(Facultad.id == recurso.facultad_id).first()
    if not facultad:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")

    # Verificar que el programa existe si se proporciona
    if recurso.programa_id:
        programa = db.query(Programa).filter(Programa.id == recurso.programa_id).first()
        if not programa:
            raise HTTPException(status_code=404, detail="Programa no encontrado")

    # Verificar que la extensión existe si se proporciona
    if recurso.extension_id:
        extension = db.query(Extension).filter(Extension.id == recurso.extension_id).first()
        if not extension:
            raise HTTPException(status_code=404, detail="Extensión no encontrada")

    # Verificar que el responsable existe
    responsable = db.query(Usuario).filter(Usuario.id == recurso.responsable_id).first()
    if not responsable:
        raise HTTPException(status_code=404, detail="Responsable no encontrado")

    # Verificar que el estado existe
    if recurso.estado_id:
        estado = db.query(Estado).filter(Estado.id == recurso.estado_id).first()
        if not estado:
            raise HTTPException(status_code=404, detail="Estado no encontrado")

    # Verificar que el tipo de estado existe
    if recurso.tipo_estado_id:
        tipo_estado = db.query(TipoEstado).filter(TipoEstado.id == recurso.tipo_estado_id).first()
        if not tipo_estado:
            raise HTTPException(status_code=404, detail="Tipo de estado no encontrado")

    # Verificar que no existe un recurso con el mismo código
    existing_recurso = db.query(RecursoModel).filter(RecursoModel.codigo == recurso.codigo).first()
    if existing_recurso:
        raise HTTPException(status_code=400, detail="Ya existe un recurso con este código")

    db_recurso = RecursoModel(**recurso.dict())
    db.add(db_recurso)
    db.commit()
    db.refresh(db_recurso)
    return db_recurso

@router.put("/{recurso_id}", response_model=Recurso)
def update_recurso(
    recurso_id: int,
    recurso: RecursoUpdate,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Actualizar un recurso existente.
    Solo administradores pueden actualizar recursos.
    """
    if current_user.rol != "Admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden actualizar recursos")

    db_recurso = db.query(RecursoModel).filter(RecursoModel.id == recurso_id).first()
    if not db_recurso:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")

    # Verificar que la facultad existe si se está actualizando
    if recurso.facultad_id:
        facultad = db.query(Facultad).filter(Facultad.id == recurso.facultad_id).first()
        if not facultad:
            raise HTTPException(status_code=404, detail="Facultad no encontrada")

    # Verificar que el programa existe si se está actualizando
    if recurso.programa_id:
        programa = db.query(Programa).filter(Programa.id == recurso.programa_id).first()
        if not programa:
            raise HTTPException(status_code=404, detail="Programa no encontrado")

    # Verificar que la extensión existe si se está actualizando
    if recurso.extension_id:
        extension = db.query(Extension).filter(Extension.id == recurso.extension_id).first()
        if not extension:
            raise HTTPException(status_code=404, detail="Extensión no encontrada")

    # Verificar que el responsable existe si se está actualizando
    if recurso.responsable_id:
        responsable = db.query(Usuario).filter(Usuario.id == recurso.responsable_id).first()
        if not responsable:
            raise HTTPException(status_code=404, detail="Responsable no encontrado")

    # Verificar que el estado existe si se está actualizando
    if recurso.estado_id:
        estado = db.query(Estado).filter(Estado.id == recurso.estado_id).first()
        if not estado:
            raise HTTPException(status_code=404, detail="Estado no encontrado")

    # Verificar que el tipo de estado existe si se está actualizando
    if recurso.tipo_estado_id:
        tipo_estado = db.query(TipoEstado).filter(TipoEstado.id == recurso.tipo_estado_id).first()
        if not tipo_estado:
            raise HTTPException(status_code=404, detail="Tipo de estado no encontrado")

    # Verificar que no existe otro recurso con el mismo código si se está actualizando
    if recurso.codigo and recurso.codigo != db_recurso.codigo:
        existing_recurso = db.query(RecursoModel).filter(RecursoModel.codigo == recurso.codigo).first()
        if existing_recurso:
            raise HTTPException(status_code=400, detail="Ya existe un recurso con este código")

    # Actualizar campos
    for key, value in recurso.dict(exclude_unset=True).items():
        setattr(db_recurso, key, value)

    db_recurso.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_recurso)
    return db_recurso

@router.delete("/{recurso_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recurso(
    recurso_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Eliminar un recurso.
    Solo administradores pueden eliminar recursos.
    """
    if current_user.rol != "Admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden eliminar recursos")

    recurso = db.query(RecursoModel).filter(RecursoModel.id == recurso_id).first()
    if not recurso:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")

    # Eliminar documentos asociados
    if recurso.documentos:
        for doc in recurso.documentos:
            doc_path = os.path.join(UPLOAD_DIR, doc)
            if os.path.exists(doc_path):
                os.remove(doc_path)

    db.delete(recurso)
    db.commit()

@router.post("/{recurso_id}/documentos")
def upload_documentos(
    recurso_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Subir documentos asociados a un recurso.
    Solo administradores pueden subir documentos.
    """
    if current_user.rol != "Admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden subir documentos")

    recurso = db.query(RecursoModel).filter(RecursoModel.id == recurso_id).first()
    if not recurso:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")

    uploaded_files = []
    for file in files:
        # Generar nombre único para el archivo
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        # Guardar archivo
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        uploaded_files.append(unique_filename)

    # Actualizar lista de documentos
    if not recurso.documentos:
        recurso.documentos = []
    recurso.documentos.extend(uploaded_files)
    recurso.fecha_actualizacion = datetime.utcnow()
    db.commit()

    return {"message": "Documentos subidos exitosamente", "files": uploaded_files}

@router.get("/estadisticas/", response_model=RecursoEstadisticas)
def get_estadisticas(
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Obtener estadísticas de recursos.
    Solo administradores pueden ver estadísticas.
    """
    if current_user.rol != "Admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden ver estadísticas")

    # Total de recursos
    total_recursos = db.query(func.count(RecursoModel.id)).scalar()

    # Recursos por tipo
    recursos_por_tipo = db.query(
        RecursoModel.tipo,
        func.count(RecursoModel.id)
    ).group_by(RecursoModel.tipo).all()
    recursos_por_tipo = dict(recursos_por_tipo)

    # Recursos por facultad
    recursos_por_facultad = db.query(
        Facultad.nombre,
        func.count(RecursoModel.id)
    ).join(RecursoModel).group_by(Facultad.nombre).all()
    recursos_por_facultad = dict(recursos_por_facultad)

    # Recursos por programa
    recursos_por_programa = db.query(
        Programa.nombre,
        func.count(RecursoModel.id)
    ).join(RecursoModel).group_by(Programa.nombre).all()
    recursos_por_programa = dict(recursos_por_programa)

    # Recursos por extensión
    recursos_por_extension = db.query(
        Extension.nombre,
        func.count(RecursoModel.id)
    ).join(RecursoModel).group_by(Extension.nombre).all()
    recursos_por_extension = dict(recursos_por_extension)

    # Recursos por estado
    recursos_por_estado = db.query(
        Estado.nombre,
        func.count(RecursoModel.id)
    ).join(RecursoModel).group_by(Estado.nombre).all()
    recursos_por_estado = dict(recursos_por_estado)

    # Recursos por responsable
    recursos_por_responsable = db.query(
        Usuario.nombre,
        func.count(RecursoModel.id)
    ).join(RecursoModel).group_by(Usuario.nombre).all()
    recursos_por_responsable = dict(recursos_por_responsable)

    # Promedio de valor
    promedio_valor = db.query(func.avg(RecursoModel.valor)).scalar() or 0

    # Total de documentos
    total_documentos = db.query(func.count(RecursoModel.documentos)).scalar()

    return RecursoEstadisticas(
        total_recursos=total_recursos,
        recursos_por_tipo=recursos_por_tipo,
        recursos_por_facultad=recursos_por_facultad,
        recursos_por_programa=recursos_por_programa,
        recursos_por_extension=recursos_por_extension,
        recursos_por_estado=recursos_por_estado,
        recursos_por_responsable=recursos_por_responsable,
        promedio_valor=promedio_valor,
        total_documentos=total_documentos
    )
