from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, extract
from typing import List, Optional
from datetime import datetime
import os
import shutil
from uuid import uuid4

from ..dependencias import get_db, get_current_user
from ..modelos import Programa as ProgramaModel, Facultad, Usuario, Estado, TipoEstado
from ..esquemas.programa import Programa, ProgramaCreate, ProgramaUpdate, ProgramaEstadisticas
from ..esquemas.usuario import Usuario as UsuarioSchema
from ..config import settings

router = APIRouter(
    prefix="/programas",
    tags=["programas"]
)

# Configuración del directorio de documentos
UPLOAD_DIR = os.path.join(settings.UPLOAD_DIR, "programas")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/", response_model=List[Programa])
def read_programas(
    facultad_id: Optional[int] = None,
    estado_id: Optional[int] = None,
    responsable_id: Optional[int] = None,
    nivel: Optional[str] = None,
    modalidad: Optional[str] = None,
    acreditacion: Optional[bool] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Obtener lista de programas con filtros opcionales.
    Solo administradores pueden ver todos los programas.
    Los usuarios normales solo ven los programas de su facultad.
    """
    query = db.query(ProgramaModel)

    # Aplicar filtros
    if facultad_id:
        query = query.filter(ProgramaModel.facultad_id == facultad_id)
    if estado_id:
        query = query.filter(ProgramaModel.estado_id == estado_id)
    if responsable_id:
        query = query.filter(ProgramaModel.responsable_id == responsable_id)
    if nivel:
        query = query.filter(ProgramaModel.nivel == nivel)
    if modalidad:
        query = query.filter(ProgramaModel.modalidad == modalidad)
    if acreditacion is not None:
        query = query.filter(ProgramaModel.acreditacion == acreditacion)
    if search:
        search_filter = or_(
            ProgramaModel.nombre.ilike(f"%{search}%"),
            ProgramaModel.descripcion.ilike(f"%{search}%"),
            ProgramaModel.codigo.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)

    # Restricción por facultad para usuarios no administradores
    if current_user.rol != "Admin":
        query = query.filter(ProgramaModel.facultad_id == current_user.facultad_id)

    programas = query.offset(skip).limit(limit).all()
    return programas

@router.get("/{programa_id}", response_model=Programa)
def read_programa(
    programa_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Obtener un programa específico por ID.
    Solo administradores pueden ver cualquier programa.
    Los usuarios normales solo pueden ver programas de su facultad.
    """
    programa = db.query(ProgramaModel).filter(ProgramaModel.id == programa_id).first()
    if not programa:
        raise HTTPException(status_code=404, detail="Programa no encontrado")

    # Verificar permisos
    if current_user.rol != "Admin" and programa.facultad_id != current_user.facultad_id:
        raise HTTPException(status_code=403, detail="No tiene permiso para ver este programa")

    return programa

@router.post("/", response_model=Programa)
def create_programa(
    programa: ProgramaCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Crear un nuevo programa.
    Solo administradores pueden crear programas.
    """
    if current_user.rol != "Admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden crear programas")

    # Verificar que la facultad existe
    facultad = db.query(Facultad).filter(Facultad.id == programa.facultad_id).first()
    if not facultad:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")

    # Verificar que el responsable existe
    responsable = db.query(Usuario).filter(Usuario.id == programa.responsable_id).first()
    if not responsable:
        raise HTTPException(status_code=404, detail="Responsable no encontrado")

    # Verificar que el estado existe
    if programa.estado_id:
        estado = db.query(Estado).filter(Estado.id == programa.estado_id).first()
        if not estado:
            raise HTTPException(status_code=404, detail="Estado no encontrado")

    # Verificar que el tipo de estado existe
    if programa.tipo_estado_id:
        tipo_estado = db.query(TipoEstado).filter(TipoEstado.id == programa.tipo_estado_id).first()
        if not tipo_estado:
            raise HTTPException(status_code=404, detail="Tipo de estado no encontrado")

    # Verificar que no existe un programa con el mismo código
    existing_programa = db.query(ProgramaModel).filter(ProgramaModel.codigo == programa.codigo).first()
    if existing_programa:
        raise HTTPException(status_code=400, detail="Ya existe un programa con este código")

    db_programa = ProgramaModel(**programa.dict())
    db.add(db_programa)
    db.commit()
    db.refresh(db_programa)
    return db_programa

@router.put("/{programa_id}", response_model=Programa)
def update_programa(
    programa_id: int,
    programa: ProgramaUpdate,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Actualizar un programa existente.
    Solo administradores pueden actualizar programas.
    """
    if current_user.rol != "Admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden actualizar programas")

    db_programa = db.query(ProgramaModel).filter(ProgramaModel.id == programa_id).first()
    if not db_programa:
        raise HTTPException(status_code=404, detail="Programa no encontrado")

    # Verificar que la facultad existe si se está actualizando
    if programa.facultad_id:
        facultad = db.query(Facultad).filter(Facultad.id == programa.facultad_id).first()
        if not facultad:
            raise HTTPException(status_code=404, detail="Facultad no encontrada")

    # Verificar que el responsable existe si se está actualizando
    if programa.responsable_id:
        responsable = db.query(Usuario).filter(Usuario.id == programa.responsable_id).first()
        if not responsable:
            raise HTTPException(status_code=404, detail="Responsable no encontrado")

    # Verificar que el estado existe si se está actualizando
    if programa.estado_id:
        estado = db.query(Estado).filter(Estado.id == programa.estado_id).first()
        if not estado:
            raise HTTPException(status_code=404, detail="Estado no encontrado")

    # Verificar que el tipo de estado existe si se está actualizando
    if programa.tipo_estado_id:
        tipo_estado = db.query(TipoEstado).filter(TipoEstado.id == programa.tipo_estado_id).first()
        if not tipo_estado:
            raise HTTPException(status_code=404, detail="Tipo de estado no encontrado")

    # Verificar que no existe otro programa con el mismo código si se está actualizando
    if programa.codigo and programa.codigo != db_programa.codigo:
        existing_programa = db.query(ProgramaModel).filter(ProgramaModel.codigo == programa.codigo).first()
        if existing_programa:
            raise HTTPException(status_code=400, detail="Ya existe un programa con este código")

    # Actualizar campos
    for key, value in programa.dict(exclude_unset=True).items():
        setattr(db_programa, key, value)

    db_programa.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_programa)
    return db_programa

@router.delete("/{programa_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_programa(
    programa_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Eliminar un programa.
    Solo administradores pueden eliminar programas.
    """
    if current_user.rol != "Admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden eliminar programas")

    programa = db.query(ProgramaModel).filter(ProgramaModel.id == programa_id).first()
    if not programa:
        raise HTTPException(status_code=404, detail="Programa no encontrado")

    # Eliminar documentos asociados
    if programa.documentos:
        for doc in programa.documentos:
            doc_path = os.path.join(UPLOAD_DIR, doc)
            if os.path.exists(doc_path):
                os.remove(doc_path)

    db.delete(programa)
    db.commit()

@router.post("/{programa_id}/documentos")
def upload_documentos(
    programa_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Subir documentos asociados a un programa.
    Solo administradores pueden subir documentos.
    """
    if current_user.rol != "Admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden subir documentos")

    programa = db.query(ProgramaModel).filter(ProgramaModel.id == programa_id).first()
    if not programa:
        raise HTTPException(status_code=404, detail="Programa no encontrado")

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
    if not programa.documentos:
        programa.documentos = []
    programa.documentos.extend(uploaded_files)
    programa.fecha_actualizacion = datetime.utcnow()
    db.commit()

    return {"message": "Documentos subidos exitosamente", "files": uploaded_files}

@router.get("/estadisticas/", response_model=ProgramaEstadisticas)
def get_estadisticas(
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Obtener estadísticas de programas.
    Solo administradores pueden ver estadísticas.
    """
    if current_user.rol != "Admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden ver estadísticas")

    # Total de programas
    total_programas = db.query(func.count(ProgramaModel.id)).scalar()

    # Programas por facultad
    programas_por_facultad = db.query(
        Facultad.nombre,
        func.count(ProgramaModel.id)
    ).join(ProgramaModel).group_by(Facultad.nombre).all()
    programas_por_facultad = dict(programas_por_facultad)

    # Programas por estado
    programas_por_estado = db.query(
        Estado.nombre,
        func.count(ProgramaModel.id)
    ).join(ProgramaModel).group_by(Estado.nombre).all()
    programas_por_estado = dict(programas_por_estado)

    # Programas por responsable
    programas_por_responsable = db.query(
        Usuario.nombre,
        func.count(ProgramaModel.id)
    ).join(ProgramaModel).group_by(Usuario.nombre).all()
    programas_por_responsable = dict(programas_por_responsable)

    # Programas por nivel
    programas_por_nivel = db.query(
        ProgramaModel.nivel,
        func.count(ProgramaModel.id)
    ).group_by(ProgramaModel.nivel).all()
    programas_por_nivel = dict(programas_por_nivel)

    # Programas por modalidad
    programas_por_modalidad = db.query(
        ProgramaModel.modalidad,
        func.count(ProgramaModel.id)
    ).group_by(ProgramaModel.modalidad).all()
    programas_por_modalidad = dict(programas_por_modalidad)

    # Programas acreditados y no acreditados
    programas_acreditados = db.query(func.count(ProgramaModel.id)).filter(ProgramaModel.acreditacion == True).scalar()
    programas_no_acreditados = db.query(func.count(ProgramaModel.id)).filter(ProgramaModel.acreditacion == False).scalar()

    # Total de extensiones
    total_extensiones = db.query(func.count(ProgramaModel.extensiones)).scalar()

    # Extensiones por programa
    extensiones_por_programa = db.query(
        ProgramaModel.nombre,
        func.count(ProgramaModel.extensiones)
    ).group_by(ProgramaModel.nombre).all()
    extensiones_por_programa = dict(extensiones_por_programa)

    # Promedios
    promedio_extensiones = total_extensiones / total_programas if total_programas > 0 else 0
    promedio_duracion = db.query(func.avg(ProgramaModel.duracion)).scalar() or 0
    promedio_creditos = db.query(func.avg(ProgramaModel.creditos)).scalar() or 0

    # Total de documentos
    total_documentos = db.query(func.count(ProgramaModel.documentos)).scalar()

    return ProgramaEstadisticas(
        total_programas=total_programas,
        programas_por_facultad=programas_por_facultad,
        programas_por_estado=programas_por_estado,
        programas_por_responsable=programas_por_responsable,
        programas_por_nivel=programas_por_nivel,
        programas_por_modalidad=programas_por_modalidad,
        programas_acreditados=programas_acreditados,
        programas_no_acreditados=programas_no_acreditados,
        total_extensiones=total_extensiones,
        extensiones_por_programa=extensiones_por_programa,
        promedio_extensiones=promedio_extensiones,
        promedio_duracion=promedio_duracion,
        promedio_creditos=promedio_creditos,
        total_documentos=total_documentos
    )
