from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, extract
from typing import List, Optional
from datetime import datetime
import os
import shutil
from uuid import uuid4

from ..dependencias import get_db, get_current_user
from ..modelos import Participante as ParticipanteModel, Usuario, Estado, TipoEstado, Extension, Programa, Facultad
from ..esquemas.participante import Participante, ParticipanteCreate, ParticipanteUpdate, ParticipanteEstadisticas
from ..esquemas.usuario import Usuario as UsuarioSchema
from ..config import settings

router = APIRouter(
    prefix="/participantes",
    tags=["participantes"]
)

# Configuración del directorio de documentos
UPLOAD_DIR = os.path.join(settings.UPLOAD_DIR, "participantes")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Roles permitidos para gestionar participantes
ROLES_PERMITIDOS = ["Admin", "Investigador"]

@router.get("/", response_model=List[Participante])
def read_participantes(
    tipo: Optional[str] = None,
    extension_id: Optional[int] = None,
    facultad_id: Optional[int] = None,
    programa_id: Optional[int] = None,
    estado_id: Optional[int] = None,
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Obtener lista de participantes con filtros opcionales.
    Administradores pueden ver todos los participantes.
    Investigadores solo ven los participantes de sus extensiones.
    """
    query = db.query(ParticipanteModel)

    # Aplicar filtros
    if tipo:
        query = query.filter(ParticipanteModel.tipo == tipo)
    if extension_id:
        query = query.filter(ParticipanteModel.extension_id == extension_id)
    if facultad_id:
        query = query.filter(ParticipanteModel.facultad_id == facultad_id)
    if programa_id:
        query = query.filter(ParticipanteModel.programa_id == programa_id)
    if estado_id:
        query = query.filter(ParticipanteModel.estado_id == estado_id)
    if fecha_inicio:
        query = query.filter(ParticipanteModel.fecha_creacion >= fecha_inicio)
    if fecha_fin:
        query = query.filter(ParticipanteModel.fecha_creacion <= fecha_fin)
    if search:
        search_filter = or_(
            ParticipanteModel.nombre.ilike(f"%{search}%"),
            ParticipanteModel.correo.ilike(f"%{search}%"),
            ParticipanteModel.rol.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)

    # Restricción por extensión para investigadores
    if current_user.rol == "Investigador":
        # Obtener las extensiones donde el usuario es investigador
        extensiones_ids = db.query(Extension.id).filter(Extension.responsable_id == current_user.id).all()
        extensiones_ids = [e[0] for e in extensiones_ids]
        query = query.filter(ParticipanteModel.extension_id.in_(extensiones_ids))

    participantes = query.offset(skip).limit(limit).all()
    return participantes

@router.get("/{participante_id}", response_model=Participante)
def read_participante(
    participante_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Obtener un participante específico por ID.
    Administradores pueden ver cualquier participante.
    Investigadores solo pueden ver participantes de sus extensiones.
    """
    participante = db.query(ParticipanteModel).filter(ParticipanteModel.id == participante_id).first()
    if not participante:
        raise HTTPException(status_code=404, detail="Participante no encontrado")

    # Verificar permisos
    if current_user.rol == "Investigador":
        # Verificar si el usuario es investigador de la extensión
        extension = db.query(Extension).filter(Extension.id == participante.extension_id).first()
        if not extension or extension.responsable_id != current_user.id:
            raise HTTPException(status_code=403, detail="No tiene permiso para ver este participante")

    return participante

@router.post("/", response_model=Participante)
def create_participante(
    participante: ParticipanteCreate,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Crear un nuevo participante.
    Solo administradores e investigadores pueden crear participantes.
    Los investigadores solo pueden crear participantes en sus extensiones.
    """
    if current_user.rol not in ROLES_PERMITIDOS:
        raise HTTPException(status_code=403, detail="No tiene permiso para crear participantes")

    # Verificar que la extensión existe
    extension = db.query(Extension).filter(Extension.id == participante.extension_id).first()
    if not extension:
        raise HTTPException(status_code=404, detail="Extensión no encontrada")

    # Verificar permisos para investigadores
    if current_user.rol == "Investigador" and extension.responsable_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tiene permiso para crear participantes en esta extensión")

    # Verificar que la facultad existe si se proporciona
    if participante.facultad_id:
        facultad = db.query(Facultad).filter(Facultad.id == participante.facultad_id).first()
        if not facultad:
            raise HTTPException(status_code=404, detail="Facultad no encontrada")

    # Verificar que el programa existe si se proporciona
    if participante.programa_id:
        programa = db.query(Programa).filter(Programa.id == participante.programa_id).first()
        if not programa:
            raise HTTPException(status_code=404, detail="Programa no encontrado")

    # Verificar que el estado existe
    if participante.estado_id:
        estado = db.query(Estado).filter(Estado.id == participante.estado_id).first()
        if not estado:
            raise HTTPException(status_code=404, detail="Estado no encontrado")

    # Verificar que el tipo de estado existe
    if participante.tipo_estado_id:
        tipo_estado = db.query(TipoEstado).filter(TipoEstado.id == participante.tipo_estado_id).first()
        if not tipo_estado:
            raise HTTPException(status_code=404, detail="Tipo de estado no encontrado")

    db_participante = ParticipanteModel(**participante.dict())
    db.add(db_participante)
    db.commit()
    db.refresh(db_participante)
    return db_participante

@router.put("/{participante_id}", response_model=Participante)
def update_participante(
    participante_id: int,
    participante: ParticipanteUpdate,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Actualizar un participante existente.
    Solo administradores e investigadores pueden actualizar participantes.
    Los investigadores solo pueden actualizar participantes de sus extensiones.
    """
    if current_user.rol not in ROLES_PERMITIDOS:
        raise HTTPException(status_code=403, detail="No tiene permiso para actualizar participantes")

    db_participante = db.query(ParticipanteModel).filter(ParticipanteModel.id == participante_id).first()
    if not db_participante:
        raise HTTPException(status_code=404, detail="Participante no encontrado")

    # Verificar permisos para investigadores
    if current_user.rol == "Investigador":
        extension = db.query(Extension).filter(Extension.id == db_participante.extension_id).first()
        if not extension or extension.responsable_id != current_user.id:
            raise HTTPException(status_code=403, detail="No tiene permiso para actualizar este participante")

    # Verificar que la extensión existe si se está actualizando
    if participante.extension_id:
        extension = db.query(Extension).filter(Extension.id == participante.extension_id).first()
        if not extension:
            raise HTTPException(status_code=404, detail="Extensión no encontrada")
        # Verificar permisos para investigadores si se cambia la extensión
        if current_user.rol == "Investigador" and extension.responsable_id != current_user.id:
            raise HTTPException(status_code=403, detail="No tiene permiso para mover el participante a esta extensión")

    # Verificar que la facultad existe si se está actualizando
    if participante.facultad_id:
        facultad = db.query(Facultad).filter(Facultad.id == participante.facultad_id).first()
        if not facultad:
            raise HTTPException(status_code=404, detail="Facultad no encontrada")

    # Verificar que el programa existe si se está actualizando
    if participante.programa_id:
        programa = db.query(Programa).filter(Programa.id == participante.programa_id).first()
        if not programa:
            raise HTTPException(status_code=404, detail="Programa no encontrado")

    # Verificar que el estado existe si se está actualizando
    if participante.estado_id:
        estado = db.query(Estado).filter(Estado.id == participante.estado_id).first()
        if not estado:
            raise HTTPException(status_code=404, detail="Estado no encontrado")

    # Verificar que el tipo de estado existe si se está actualizando
    if participante.tipo_estado_id:
        tipo_estado = db.query(TipoEstado).filter(TipoEstado.id == participante.tipo_estado_id).first()
        if not tipo_estado:
            raise HTTPException(status_code=404, detail="Tipo de estado no encontrado")

    # Actualizar campos
    for key, value in participante.dict(exclude_unset=True).items():
        setattr(db_participante, key, value)

    db_participante.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_participante)
    return db_participante

@router.delete("/{participante_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_participante(
    participante_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Eliminar un participante.
    Solo administradores e investigadores pueden eliminar participantes.
    Los investigadores solo pueden eliminar participantes de sus extensiones.
    """
    if current_user.rol not in ROLES_PERMITIDOS:
        raise HTTPException(status_code=403, detail="No tiene permiso para eliminar participantes")

    participante = db.query(ParticipanteModel).filter(ParticipanteModel.id == participante_id).first()
    if not participante:
        raise HTTPException(status_code=404, detail="Participante no encontrado")

    # Verificar permisos para investigadores
    if current_user.rol == "Investigador":
        extension = db.query(Extension).filter(Extension.id == participante.extension_id).first()
        if not extension or extension.responsable_id != current_user.id:
            raise HTTPException(status_code=403, detail="No tiene permiso para eliminar este participante")

    # Eliminar documentos asociados
    if participante.documentos:
        for doc in participante.documentos:
            doc_path = os.path.join(UPLOAD_DIR, doc)
            if os.path.exists(doc_path):
                os.remove(doc_path)

    db.delete(participante)
    db.commit()

@router.post("/{participante_id}/documentos")
def upload_documentos(
    participante_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Subir documentos asociados a un participante.
    Solo administradores e investigadores pueden subir documentos.
    Los investigadores solo pueden subir documentos para participantes de sus extensiones.
    """
    if current_user.rol not in ROLES_PERMITIDOS:
        raise HTTPException(status_code=403, detail="No tiene permiso para subir documentos")

    participante = db.query(ParticipanteModel).filter(ParticipanteModel.id == participante_id).first()
    if not participante:
        raise HTTPException(status_code=404, detail="Participante no encontrado")

    # Verificar permisos para investigadores
    if current_user.rol == "Investigador":
        extension = db.query(Extension).filter(Extension.id == participante.extension_id).first()
        if not extension or extension.responsable_id != current_user.id:
            raise HTTPException(status_code=403, detail="No tiene permiso para subir documentos para este participante")

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
    if not participante.documentos:
        participante.documentos = []
    participante.documentos.extend(uploaded_files)
    participante.fecha_actualizacion = datetime.utcnow()
    db.commit()

    return {"message": "Documentos subidos exitosamente", "files": uploaded_files}

@router.get("/estadisticas/", response_model=ParticipanteEstadisticas)
def get_estadisticas(
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Obtener estadísticas de participantes.
    Solo administradores pueden ver estadísticas globales.
    Los investigadores solo ven estadísticas de sus extensiones.
    """
    if current_user.rol not in ROLES_PERMITIDOS:
        raise HTTPException(status_code=403, detail="No tiene permiso para ver estadísticas")

    # Base query
    query = db.query(ParticipanteModel)

    # Filtrar por extensiones del investigador si no es admin
    if current_user.rol == "Investigador":
        extensiones_ids = db.query(Extension.id).filter(Extension.responsable_id == current_user.id).all()
        extensiones_ids = [e[0] for e in extensiones_ids]
        query = query.filter(ParticipanteModel.extension_id.in_(extensiones_ids))

    # Total de participantes
    total_participantes = query.count()

    # Participantes por tipo
    participantes_por_tipo = query.with_entities(
        ParticipanteModel.tipo,
        func.count(ParticipanteModel.id)
    ).group_by(ParticipanteModel.tipo).all()
    participantes_por_tipo = dict(participantes_por_tipo)

    # Participantes por extensión
    participantes_por_extension = query.join(Extension).with_entities(
        Extension.nombre,
        func.count(ParticipanteModel.id)
    ).group_by(Extension.nombre).all()
    participantes_por_extension = dict(participantes_por_extension)

    # Participantes por facultad
    participantes_por_facultad = query.join(Facultad).with_entities(
        Facultad.nombre,
        func.count(ParticipanteModel.id)
    ).group_by(Facultad.nombre).all()
    participantes_por_facultad = dict(participantes_por_facultad)

    # Participantes por programa
    participantes_por_programa = query.join(Programa).with_entities(
        Programa.nombre,
        func.count(ParticipanteModel.id)
    ).group_by(Programa.nombre).all()
    participantes_por_programa = dict(participantes_por_programa)

    # Participantes por estado
    participantes_por_estado = query.join(Estado).with_entities(
        Estado.nombre,
        func.count(ParticipanteModel.id)
    ).group_by(Estado.nombre).all()
    participantes_por_estado = dict(participantes_por_estado)

    # Participantes por rol
    participantes_por_rol = query.with_entities(
        ParticipanteModel.rol,
        func.count(ParticipanteModel.id)
    ).group_by(ParticipanteModel.rol).all()
    participantes_por_rol = dict(participantes_por_rol)

    # Promedio de horas de participación
    promedio_horas = query.with_entities(func.avg(ParticipanteModel.horas_participacion)).scalar() or 0

    # Total de certificados
    total_certificados = query.filter(ParticipanteModel.certificado == True).count()

    # Total de documentos
    total_documentos = query.filter(ParticipanteModel.documentos != None).count()

    return ParticipanteEstadisticas(
        total_participantes=total_participantes,
        participantes_por_tipo=participantes_por_tipo,
        participantes_por_extension=participantes_por_extension,
        participantes_por_facultad=participantes_por_facultad,
        participantes_por_programa=participantes_por_programa,
        participantes_por_estado=participantes_por_estado,
        participantes_por_rol=participantes_por_rol,
        promedio_horas_participacion=promedio_horas,
        total_certificados=total_certificados,
        total_documentos=total_documentos
    )
