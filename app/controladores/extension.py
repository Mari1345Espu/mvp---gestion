from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, extract
from typing import List, Optional
from datetime import datetime
import os
import shutil
from uuid import uuid4

from ..dependencias import get_db, get_current_user
from ..modelos import Extension as ExtensionModel, Facultad, Programa, Usuario, Estado, TipoEstado
from ..esquemas.extension import Extension, ExtensionCreate, ExtensionUpdate, ExtensionEstadisticas
from ..esquemas.usuario import Usuario as UsuarioSchema
from ..config import settings

router = APIRouter(
    prefix="/extensiones",
    tags=["extensiones"]
)

# Configuración del directorio de documentos
UPLOAD_DIR = os.path.join(settings.UPLOAD_DIR, "extensiones")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/", response_model=List[Extension])
def read_extensiones(
    facultad_id: Optional[int] = None,
    programa_id: Optional[int] = None,
    estado_id: Optional[int] = None,
    responsable_id: Optional[int] = None,
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Obtener lista de extensiones con filtros opcionales.
    Solo administradores pueden ver todas las extensiones.
    Los usuarios normales solo ven las extensiones de su facultad.
    """
    query = db.query(ExtensionModel)

    # Aplicar filtros
    if facultad_id:
        query = query.filter(ExtensionModel.facultad_id == facultad_id)
    if programa_id:
        query = query.filter(ExtensionModel.programa_id == programa_id)
    if estado_id:
        query = query.filter(ExtensionModel.estado_id == estado_id)
    if responsable_id:
        query = query.filter(ExtensionModel.responsable_id == responsable_id)
    if fecha_inicio:
        query = query.filter(ExtensionModel.fecha_creacion >= fecha_inicio)
    if fecha_fin:
        query = query.filter(ExtensionModel.fecha_creacion <= fecha_fin)
    if search:
        search_filter = or_(
            ExtensionModel.nombre.ilike(f"%{search}%"),
            ExtensionModel.descripcion.ilike(f"%{search}%"),
            ExtensionModel.codigo.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)

    # Restricción por facultad para usuarios no administradores
    if current_user.rol != "Admin":
        query = query.filter(ExtensionModel.facultad_id == current_user.facultad_id)

    extensiones = query.offset(skip).limit(limit).all()
    return extensiones

@router.get("/{extension_id}", response_model=Extension)
def read_extension(
    extension_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Obtener una extensión específica por ID.
    Solo administradores pueden ver cualquier extensión.
    Los usuarios normales solo pueden ver extensiones de su facultad.
    """
    extension = db.query(ExtensionModel).filter(ExtensionModel.id == extension_id).first()
    if not extension:
        raise HTTPException(status_code=404, detail="Extensión no encontrada")

    # Verificar permisos
    if current_user.rol != "Admin" and extension.facultad_id != current_user.facultad_id:
        raise HTTPException(status_code=403, detail="No tiene permiso para ver esta extensión")

    return extension

@router.post("/", response_model=Extension)
def create_extension(
    extension: ExtensionCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Crear una nueva extensión.
    Solo administradores pueden crear extensiones.
    """
    if current_user.rol != "Admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden crear extensiones")

    # Verificar que la facultad existe
    facultad = db.query(Facultad).filter(Facultad.id == extension.facultad_id).first()
    if not facultad:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")

    # Verificar que el programa existe
    programa = db.query(Programa).filter(Programa.id == extension.programa_id).first()
    if not programa:
        raise HTTPException(status_code=404, detail="Programa no encontrado")

    # Verificar que el responsable existe
    responsable = db.query(Usuario).filter(Usuario.id == extension.responsable_id).first()
    if not responsable:
        raise HTTPException(status_code=404, detail="Responsable no encontrado")

    # Verificar que el estado existe
    if extension.estado_id:
        estado = db.query(Estado).filter(Estado.id == extension.estado_id).first()
        if not estado:
            raise HTTPException(status_code=404, detail="Estado no encontrado")

    # Verificar que el tipo de estado existe
    if extension.tipo_estado_id:
        tipo_estado = db.query(TipoEstado).filter(TipoEstado.id == extension.tipo_estado_id).first()
        if not tipo_estado:
            raise HTTPException(status_code=404, detail="Tipo de estado no encontrado")

    # Verificar que no existe una extensión con el mismo código
    existing_extension = db.query(ExtensionModel).filter(ExtensionModel.codigo == extension.codigo).first()
    if existing_extension:
        raise HTTPException(status_code=400, detail="Ya existe una extensión con este código")

    db_extension = ExtensionModel(**extension.dict())
    db.add(db_extension)
    db.commit()
    db.refresh(db_extension)
    return db_extension

@router.put("/{extension_id}", response_model=Extension)
def update_extension(
    extension_id: int,
    extension: ExtensionUpdate,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Actualizar una extensión existente.
    Solo administradores pueden actualizar extensiones.
    """
    if current_user.rol != "Admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden actualizar extensiones")

    db_extension = db.query(ExtensionModel).filter(ExtensionModel.id == extension_id).first()
    if not db_extension:
        raise HTTPException(status_code=404, detail="Extensión no encontrada")

    # Verificar que la facultad existe si se está actualizando
    if extension.facultad_id:
        facultad = db.query(Facultad).filter(Facultad.id == extension.facultad_id).first()
        if not facultad:
            raise HTTPException(status_code=404, detail="Facultad no encontrada")

    # Verificar que el programa existe si se está actualizando
    if extension.programa_id:
        programa = db.query(Programa).filter(Programa.id == extension.programa_id).first()
        if not programa:
            raise HTTPException(status_code=404, detail="Programa no encontrado")

    # Verificar que el responsable existe si se está actualizando
    if extension.responsable_id:
        responsable = db.query(Usuario).filter(Usuario.id == extension.responsable_id).first()
        if not responsable:
            raise HTTPException(status_code=404, detail="Responsable no encontrado")

    # Verificar que el estado existe si se está actualizando
    if extension.estado_id:
        estado = db.query(Estado).filter(Estado.id == extension.estado_id).first()
        if not estado:
            raise HTTPException(status_code=404, detail="Estado no encontrado")

    # Verificar que el tipo de estado existe si se está actualizando
    if extension.tipo_estado_id:
        tipo_estado = db.query(TipoEstado).filter(TipoEstado.id == extension.tipo_estado_id).first()
        if not tipo_estado:
            raise HTTPException(status_code=404, detail="Tipo de estado no encontrado")

    # Verificar que no existe otra extensión con el mismo código si se está actualizando
    if extension.codigo and extension.codigo != db_extension.codigo:
        existing_extension = db.query(ExtensionModel).filter(ExtensionModel.codigo == extension.codigo).first()
        if existing_extension:
            raise HTTPException(status_code=400, detail="Ya existe una extensión con este código")

    # Actualizar campos
    for key, value in extension.dict(exclude_unset=True).items():
        setattr(db_extension, key, value)

    db_extension.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_extension)
    return db_extension

@router.delete("/{extension_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_extension(
    extension_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Eliminar una extensión.
    Solo administradores pueden eliminar extensiones.
    """
    if current_user.rol != "Admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden eliminar extensiones")

    extension = db.query(ExtensionModel).filter(ExtensionModel.id == extension_id).first()
    if not extension:
        raise HTTPException(status_code=404, detail="Extensión no encontrada")

    # Eliminar documentos asociados
    if extension.documentos:
        for doc in extension.documentos:
            doc_path = os.path.join(UPLOAD_DIR, doc)
            if os.path.exists(doc_path):
                os.remove(doc_path)

    db.delete(extension)
    db.commit()

@router.post("/{extension_id}/documentos")
def upload_documentos(
    extension_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Subir documentos asociados a una extensión.
    Solo administradores pueden subir documentos.
    """
    if current_user.rol != "Admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden subir documentos")

    extension = db.query(ExtensionModel).filter(ExtensionModel.id == extension_id).first()
    if not extension:
        raise HTTPException(status_code=404, detail="Extensión no encontrada")

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
    if not extension.documentos:
        extension.documentos = []
    extension.documentos.extend(uploaded_files)
    extension.fecha_actualizacion = datetime.utcnow()
    db.commit()

    return {"message": "Documentos subidos exitosamente", "files": uploaded_files}

@router.get("/estadisticas/", response_model=ExtensionEstadisticas)
def get_estadisticas(
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Obtener estadísticas de extensiones.
    Solo administradores pueden ver estadísticas.
    """
    if current_user.rol != "Admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden ver estadísticas")

    # Total de extensiones
    total_extensiones = db.query(func.count(ExtensionModel.id)).scalar()

    # Extensiones por facultad
    extensiones_por_facultad = db.query(
        Facultad.nombre,
        func.count(ExtensionModel.id)
    ).join(ExtensionModel).group_by(Facultad.nombre).all()
    extensiones_por_facultad = dict(extensiones_por_facultad)

    # Extensiones por programa
    extensiones_por_programa = db.query(
        Programa.nombre,
        func.count(ExtensionModel.id)
    ).join(ExtensionModel).group_by(Programa.nombre).all()
    extensiones_por_programa = dict(extensiones_por_programa)

    # Extensiones por estado
    extensiones_por_estado = db.query(
        Estado.nombre,
        func.count(ExtensionModel.id)
    ).join(ExtensionModel).group_by(Estado.nombre).all()
    extensiones_por_estado = dict(extensiones_por_estado)

    # Extensiones por responsable
    extensiones_por_responsable = db.query(
        Usuario.nombre,
        func.count(ExtensionModel.id)
    ).join(ExtensionModel).group_by(Usuario.nombre).all()
    extensiones_por_responsable = dict(extensiones_por_responsable)

    # Promedio de presupuesto
    promedio_presupuesto = db.query(func.avg(ExtensionModel.presupuesto)).scalar() or 0

    # Promedio de impacto
    promedio_impacto = db.query(func.avg(ExtensionModel.impacto)).scalar() or 0

    # Total de documentos
    total_documentos = db.query(func.count(ExtensionModel.documentos)).scalar()

    return ExtensionEstadisticas(
        total_extensiones=total_extensiones,
        extensiones_por_facultad=extensiones_por_facultad,
        extensiones_por_programa=extensiones_por_programa,
        extensiones_por_estado=extensiones_por_estado,
        extensiones_por_responsable=extensiones_por_responsable,
        promedio_presupuesto=promedio_presupuesto,
        promedio_impacto=promedio_impacto,
        total_documentos=total_documentos
    )
