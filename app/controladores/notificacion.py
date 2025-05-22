from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, extract
from typing import List, Optional
from datetime import datetime, timedelta
import json

from app import modelos
from app.db.session import get_db
from app.core.seguridad import get_current_user
from app.core.email import send_notification_email

from app.esquemas.notificacion import (
    Notificacion, NotificacionCreate, NotificacionUpdate, NotificacionEstadisticas,
    TipoNotificacion, PrioridadNotificacion, EstadoNotificacion
)
from app.esquemas.usuario import Usuario as UsuarioSchema
from app.config import settings

router = APIRouter(
    prefix="/notificaciones",
    tags=["notificaciones"]
)

# Roles permitidos para gestionar notificaciones
ROLES_PERMITIDOS = ["Admin", "Investigador", "Evaluador", "Asesor"]

async def enviar_notificacion_email(usuario: modelos.Usuario, notificacion: modelos.Notificacion):
    """
    Función para enviar notificaciones por correo electrónico.
    Se implementará la lógica de envío de correos aquí.
    """
    # TODO: Implementar lógica de envío de correos
    pass

@router.get("/", response_model=List[Notificacion])
def read_notificaciones(
    tipo: Optional[TipoNotificacion] = None,
    prioridad: Optional[PrioridadNotificacion] = None,
    estado: Optional[EstadoNotificacion] = None,
    entidad_id: Optional[int] = None,
    entidad_tipo: Optional[str] = None,
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Obtener lista de notificaciones con filtros opcionales.
    Los usuarios solo ven sus propias notificaciones.
    Los administradores pueden ver todas las notificaciones.
    """
    query = db.query(modelos.Notificacion)

    # Aplicar filtros
    if tipo:
        query = query.filter(modelos.Notificacion.tipo == tipo)
    if prioridad:
        query = query.filter(modelos.Notificacion.prioridad == prioridad)
    if estado:
        query = query.filter(modelos.Notificacion.estado == estado)
    if entidad_id:
        query = query.filter(modelos.Notificacion.entidad_id == entidad_id)
    if entidad_tipo:
        query = query.filter(modelos.Notificacion.entidad_tipo == entidad_tipo)
    if fecha_inicio:
        query = query.filter(modelos.Notificacion.fecha_creacion >= fecha_inicio)
    if fecha_fin:
        query = query.filter(modelos.Notificacion.fecha_creacion <= fecha_fin)
    if search:
        search_filter = or_(
            modelos.Notificacion.titulo.ilike(f"%{search}%"),
            modelos.Notificacion.mensaje.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)

    # Restricción por usuario si no es administrador
    if current_user.rol != "Admin":
        query = query.filter(modelos.Notificacion.usuario_id == current_user.id)

    # Ordenar por fecha de creación descendente
    query = query.order_by(modelos.Notificacion.fecha_creacion.desc())

    notificaciones = query.offset(skip).limit(limit).all()
    return notificaciones

@router.get("/{notificacion_id}", response_model=Notificacion)
def read_notificacion(
    notificacion_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Obtener una notificación específica por ID.
    Los usuarios solo pueden ver sus propias notificaciones.
    Los administradores pueden ver cualquier notificación.
    """
    notificacion = db.query(modelos.Notificacion).filter(modelos.Notificacion.id == notificacion_id).first()
    if not notificacion:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")

    # Verificar permisos
    if current_user.rol != "Admin" and notificacion.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tiene permiso para ver esta notificación")

    # Marcar como leída si no lo está
    if notificacion.estado == EstadoNotificacion.NO_LEIDA:
        notificacion.estado = EstadoNotificacion.LEIDA
        notificacion.fecha_lectura = datetime.utcnow()
        db.commit()

    return notificacion

@router.post("/", response_model=Notificacion)
async def create_notificacion(
    notificacion: NotificacionCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Crear una nueva notificación.
    Solo administradores pueden crear notificaciones para otros usuarios.
    Los usuarios normales solo pueden crear notificaciones para sí mismos.
    """
    if current_user.rol not in ROLES_PERMITIDOS:
        raise HTTPException(status_code=403, detail="No tiene permiso para crear notificaciones")

    # Verificar que el usuario existe
    usuario = db.query(modelos.Usuario).filter(modelos.Usuario.id == notificacion.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Verificar permisos
    if current_user.rol != "Admin" and notificacion.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tiene permiso para crear notificaciones para otros usuarios")

    db_notificacion = modelos.Notificacion(**notificacion.dict())
    db.add(db_notificacion)
    db.commit()
    db.refresh(db_notificacion)

    # Enviar notificación por correo en segundo plano
    background_tasks.add_task(enviar_notificacion_email, usuario, db_notificacion)

    return db_notificacion

@router.put("/{notificacion_id}", response_model=Notificacion)
def update_notificacion(
    notificacion_id: int,
    notificacion: NotificacionUpdate,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Actualizar una notificación existente.
    Solo administradores pueden actualizar notificaciones.
    """
    if current_user.rol != "Admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden actualizar notificaciones")

    db_notificacion = db.query(modelos.Notificacion).filter(modelos.Notificacion.id == notificacion_id).first()
    if not db_notificacion:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")

    # Actualizar campos
    for key, value in notificacion.dict(exclude_unset=True).items():
        setattr(db_notificacion, key, value)

    db_notificacion.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_notificacion)
    return db_notificacion

@router.delete("/{notificacion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notificacion(
    notificacion_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Eliminar una notificación.
    Solo administradores pueden eliminar notificaciones.
    """
    if current_user.rol != "Admin":
        raise HTTPException(status_code=403, detail="Solo los administradores pueden eliminar notificaciones")

    notificacion = db.query(modelos.Notificacion).filter(modelos.Notificacion.id == notificacion_id).first()
    if not notificacion:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")

    db.delete(notificacion)
    db.commit()

@router.post("/{notificacion_id}/marcar-leida")
def marcar_como_leida(
    notificacion_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Marcar una notificación como leída.
    Los usuarios solo pueden marcar sus propias notificaciones como leídas.
    """
    notificacion = db.query(modelos.Notificacion).filter(modelos.Notificacion.id == notificacion_id).first()
    if not notificacion:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")

    # Verificar permisos
    if current_user.rol != "Admin" and notificacion.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tiene permiso para marcar esta notificación como leída")

    notificacion.estado = EstadoNotificacion.LEIDA
    notificacion.fecha_lectura = datetime.utcnow()
    db.commit()

    return {"message": "Notificación marcada como leída"}

@router.post("/{notificacion_id}/archivar")
def archivar_notificacion(
    notificacion_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Archivar una notificación.
    Los usuarios solo pueden archivar sus propias notificaciones.
    """
    notificacion = db.query(modelos.Notificacion).filter(modelos.Notificacion.id == notificacion_id).first()
    if not notificacion:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")

    # Verificar permisos
    if current_user.rol != "Admin" and notificacion.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tiene permiso para archivar esta notificación")

    notificacion.estado = EstadoNotificacion.ARCHIVADA
    db.commit()

    return {"message": "Notificación archivada"}

@router.get("/estadisticas/", response_model=NotificacionEstadisticas)
def get_estadisticas(
    db: Session = Depends(get_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Obtener estadísticas de notificaciones.
    Solo administradores pueden ver estadísticas globales.
    Los usuarios normales solo ven estadísticas de sus propias notificaciones.
    """
    if current_user.rol not in ROLES_PERMITIDOS:
        raise HTTPException(status_code=403, detail="No tiene permiso para ver estadísticas")

    # Base query
    query = db.query(modelos.Notificacion)

    # Filtrar por usuario si no es admin
    if current_user.rol != "Admin":
        query = query.filter(modelos.Notificacion.usuario_id == current_user.id)

    # Total de notificaciones
    total_notificaciones = query.count()

    # Notificaciones por tipo
    notificaciones_por_tipo = query.with_entities(
        modelos.Notificacion.tipo,
        func.count(modelos.Notificacion.id)
    ).group_by(modelos.Notificacion.tipo).all()
    notificaciones_por_tipo = dict(notificaciones_por_tipo)

    # Notificaciones por prioridad
    notificaciones_por_prioridad = query.with_entities(
        modelos.Notificacion.prioridad,
        func.count(modelos.Notificacion.id)
    ).group_by(modelos.Notificacion.prioridad).all()
    notificaciones_por_prioridad = dict(notificaciones_por_prioridad)

    # Notificaciones por estado
    notificaciones_por_estado = query.with_entities(
        modelos.Notificacion.estado,
        func.count(modelos.Notificacion.id)
    ).group_by(modelos.Notificacion.estado).all()
    notificaciones_por_estado = dict(notificaciones_por_estado)

    # Notificaciones por usuario
    notificaciones_por_usuario = query.join(modelos.Usuario).with_entities(
        modelos.Usuario.nombre,
        func.count(modelos.Notificacion.id)
    ).group_by(modelos.Usuario.nombre).all()
    notificaciones_por_usuario = dict(notificaciones_por_usuario)

    # Notificaciones no leídas
    notificaciones_no_leidas = query.filter(
        modelos.Notificacion.estado == EstadoNotificacion.NO_LEIDA
    ).count()

    # Notificaciones urgentes
    notificaciones_urgentes = query.filter(
        modelos.Notificacion.prioridad == PrioridadNotificacion.URGENTE
    ).count()

    # Promedio de tiempo de lectura
    notificaciones_leidas = query.filter(
        modelos.Notificacion.estado == EstadoNotificacion.LEIDA,
        modelos.Notificacion.fecha_lectura != None
    ).all()
    
    if notificaciones_leidas:
        tiempo_total = sum(
            (n.fecha_lectura - n.fecha_creacion).total_seconds() / 3600
            for n in notificaciones_leidas
        )
        promedio_tiempo = tiempo_total / len(notificaciones_leidas)
    else:
        promedio_tiempo = 0

    # Notificaciones expiradas
    notificaciones_expiradas = query.filter(
        modelos.Notificacion.fecha_expiracion < datetime.utcnow()
    ).count()

    return NotificacionEstadisticas(
        total_notificaciones=total_notificaciones,
        notificaciones_por_tipo=notificaciones_por_tipo,
        notificaciones_por_prioridad=notificaciones_por_prioridad,
        notificaciones_por_estado=notificaciones_por_estado,
        notificaciones_por_usuario=notificaciones_por_usuario,
        notificaciones_no_leidas=notificaciones_no_leidas,
        notificaciones_urgentes=notificaciones_urgentes,
        promedio_tiempo_lectura=promedio_tiempo,
        notificaciones_expiradas=notificaciones_expiradas
    )
