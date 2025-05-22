from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, extract
from typing import List, Optional
from datetime import datetime
import os
import shutil
from uuid import uuid4

from ..dependencias import get_db, get_current_user
from ..modelos import Facultad as FacultadModel, Usuario, Estado, TipoEstado, Programa
from ..esquemas.facultad import Facultad, FacultadCreate, FacultadUpdate, FacultadEstadisticas
from ..esquemas.usuario import Usuario as UsuarioSchema
from ..config import settings

router = APIRouter(
    prefix="/facultades",
    tags=["facultades"]
)

# Configuración del directorio de documentos
UPLOAD_DIR = os.path.join(settings.UPLOAD_DIR, "facultades")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/", response_model=List[Facultad])
def read_facultades(
    estado_id: Optional[int] = None,
    responsable_id: Optional[int] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Obtener lista de facultades con filtros opcionales.
    Solo administradores pueden ver todas las facultades.
    Los usuarios normales solo ven su facultad asignada.
    """
    query = db.query(FacultadModel)

    # Aplicar filtros
    if estado_id:
        query = query.filter(FacultadModel.estado_id == estado_id)
    if responsable_id:
        query = query.filter(FacultadModel.responsable_id == responsable_id)
    if search:
        search_filter = or_(
            FacultadModel.nombre.ilike(f"%{search}%"),
            FacultadModel.descripcion.ilike(f"%{search}%"),
            FacultadModel.codigo.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)

    # Restricción para usuarios no administradores
    if current_user.rol != "Admin":
        query = query.filter(FacultadModel.id == current_user.facultad_id)

    facultades = query.offset(skip).limit(limit).all()
    return facultades

@router.get("/{facultad_id}", response_model=Facultad)
def read_facultad(
    facultad_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Obtener una facultad específica por ID.
    Solo administradores pueden ver cualquier facultad.
    Los usuarios normales solo pueden ver su facultad asignada.
    """
    facultad = db.query(FacultadModel).filter(FacultadModel.id == facultad_id).first()
    if not facultad:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")

    # Verificar permisos
    if current_user.rol != "Admin" and facultad.id != current_user.facultad_id:
        raise HTTPException(status_code=403, detail="No tiene permiso para ver esta facultad")

    return facultad

@router.post("/", response_model=Facultad)
def create_facultad(
    facultad: FacultadCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Crear una nueva facultad.
    Solo administradores pueden crear facultades.
    """
    if current_user.rol != "Admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden crear facultades")

    # Verificar que el responsable existe
    responsable = db.query(Usuario).filter(Usuario.id == facultad.responsable_id).first()
    if not responsable:
        raise HTTPException(status_code=404, detail="Responsable no encontrado")

    # Verificar que el estado existe
    if facultad.estado_id:
        estado = db.query(Estado).filter(Estado.id == facultad.estado_id).first()
        if not estado:
            raise HTTPException(status_code=404, detail="Estado no encontrado")

    # Verificar que el tipo de estado existe
    if facultad.tipo_estado_id:
        tipo_estado = db.query(TipoEstado).filter(TipoEstado.id == facultad.tipo_estado_id).first()
        if not tipo_estado:
            raise HTTPException(status_code=404, detail="Tipo de estado no encontrado")

    # Verificar que no existe una facultad con el mismo código
    existing_facultad = db.query(FacultadModel).filter(FacultadModel.codigo == facultad.codigo).first()
    if existing_facultad:
        raise HTTPException(status_code=400, detail="Ya existe una facultad con este código")

    db_facultad = FacultadModel(**facultad.dict())
    db.add(db_facultad)
    db.commit()
    db.refresh(db_facultad)
    return db_facultad

@router.put("/{facultad_id}", response_model=Facultad)
def update_facultad(
    facultad_id: int,
    facultad: FacultadUpdate,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Actualizar una facultad existente.
    Solo administradores pueden actualizar facultades.
    """
    if current_user.rol != "Admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden actualizar facultades")

    db_facultad = db.query(FacultadModel).filter(FacultadModel.id == facultad_id).first()
    if not db_facultad:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")

    # Verificar que el responsable existe si se está actualizando
    if facultad.responsable_id:
        responsable = db.query(Usuario).filter(Usuario.id == facultad.responsable_id).first()
        if not responsable:
            raise HTTPException(status_code=404, detail="Responsable no encontrado")

    # Verificar que el estado existe si se está actualizando
    if facultad.estado_id:
        estado = db.query(Estado).filter(Estado.id == facultad.estado_id).first()
        if not estado:
            raise HTTPException(status_code=404, detail="Estado no encontrado")

    # Verificar que el tipo de estado existe si se está actualizando
    if facultad.tipo_estado_id:
        tipo_estado = db.query(TipoEstado).filter(TipoEstado.id == facultad.tipo_estado_id).first()
        if not tipo_estado:
            raise HTTPException(status_code=404, detail="Tipo de estado no encontrado")

    # Verificar que no existe otra facultad con el mismo código si se está actualizando
    if facultad.codigo and facultad.codigo != db_facultad.codigo:
        existing_facultad = db.query(FacultadModel).filter(FacultadModel.codigo == facultad.codigo).first()
        if existing_facultad:
            raise HTTPException(status_code=400, detail="Ya existe una facultad con este código")

    # Actualizar campos
    for key, value in facultad.dict(exclude_unset=True).items():
        setattr(db_facultad, key, value)

    db_facultad.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_facultad)
    return db_facultad

@router.delete("/{facultad_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_facultad(
    facultad_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Eliminar una facultad.
    Solo administradores pueden eliminar facultades.
    """
    if current_user.rol != "Admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden eliminar facultades")

    facultad = db.query(FacultadModel).filter(FacultadModel.id == facultad_id).first()
    if not facultad:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")

    # Verificar que no hay programas asociados
    programas = db.query(Programa).filter(Programa.facultad_id == facultad_id).first()
    if programas:
        raise HTTPException(status_code=400, detail="No se puede eliminar la facultad porque tiene programas asociados")

    # Eliminar documentos asociados
    if facultad.documentos:
        for doc in facultad.documentos:
            doc_path = os.path.join(UPLOAD_DIR, doc)
            if os.path.exists(doc_path):
                os.remove(doc_path)

    db.delete(facultad)
    db.commit()

@router.post("/{facultad_id}/documentos")
def upload_documentos(
    facultad_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Subir documentos asociados a una facultad.
    Solo administradores pueden subir documentos.
    """
    if current_user.rol != "Admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden subir documentos")

    facultad = db.query(FacultadModel).filter(FacultadModel.id == facultad_id).first()
    if not facultad:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")

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
    if not facultad.documentos:
        facultad.documentos = []
    facultad.documentos.extend(uploaded_files)
    facultad.fecha_actualizacion = datetime.utcnow()
    db.commit()

    return {"message": "Documentos subidos exitosamente", "files": uploaded_files}

@router.get("/estadisticas/", response_model=FacultadEstadisticas)
def get_estadisticas(
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Obtener estadísticas de facultades.
    Solo administradores pueden ver estadísticas.
    """
    if current_user.rol != "Admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden ver estadísticas")

    # Total de facultades
    total_facultades = db.query(func.count(FacultadModel.id)).scalar()

    # Facultades por estado
    facultades_por_estado = db.query(
        Estado.nombre,
        func.count(FacultadModel.id)
    ).join(FacultadModel).group_by(Estado.nombre).all()
    facultades_por_estado = dict(facultades_por_estado)

    # Facultades por responsable
    facultades_por_responsable = db.query(
        Usuario.nombre,
        func.count(FacultadModel.id)
    ).join(FacultadModel).group_by(Usuario.nombre).all()
    facultades_por_responsable = dict(facultades_por_responsable)

    # Total de programas
    total_programas = db.query(func.count(Programa.id)).scalar()

    # Programas por facultad
    programas_por_facultad = db.query(
        FacultadModel.nombre,
        func.count(Programa.id)
    ).join(Programa).group_by(FacultadModel.nombre).all()
    programas_por_facultad = dict(programas_por_facultad)

    # Promedio de programas por facultad
    promedio_programas = total_programas / total_facultades if total_facultades > 0 else 0

    # Total de documentos
    total_documentos = db.query(func.count(FacultadModel.documentos)).scalar()

    return FacultadEstadisticas(
        total_facultades=total_facultades,
        facultades_por_estado=facultades_por_estado,
        facultades_por_responsable=facultades_por_responsable,
        total_programas=total_programas,
        programas_por_facultad=programas_por_facultad,
        promedio_programas=promedio_programas,
        total_documentos=total_documentos
    )
