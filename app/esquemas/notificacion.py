from pydantic import BaseModel, constr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class TipoNotificacion(str, Enum):
    EXTENSION = "extension"
    PARTICIPANTE = "participante"
    RECURSO = "recurso"
    EVALUACION = "evaluacion"
    DOCUMENTO = "documento"
    SISTEMA = "sistema"

class PrioridadNotificacion(str, Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    URGENTE = "urgente"

class EstadoNotificacion(str, Enum):
    NO_LEIDA = "no_leida"
    LEIDA = "leida"
    ARCHIVADA = "archivada"

class NotificacionBase(BaseModel):
    titulo: constr(min_length=3, max_length=100)
    mensaje: constr(min_length=10, max_length=500)
    tipo: TipoNotificacion
    prioridad: PrioridadNotificacion = PrioridadNotificacion.MEDIA
    estado: EstadoNotificacion = EstadoNotificacion.NO_LEIDA
    usuario_id: int
    entidad_id: Optional[int] = None  # ID de la entidad relacionada (extension, participante, etc.)
    entidad_tipo: Optional[str] = None  # Tipo de entidad relacionada
    datos_adicionales: Optional[Dict[str, Any]] = None
    fecha_expiracion: Optional[datetime] = None
    accion_url: Optional[str] = None  # URL para realizar una acción relacionada
    accion_texto: Optional[str] = None  # Texto descriptivo de la acción

class NotificacionCreate(NotificacionBase):
    pass

class NotificacionUpdate(BaseModel):
    titulo: Optional[constr(min_length=3, max_length=100)] = None
    mensaje: Optional[constr(min_length=10, max_length=500)] = None
    tipo: Optional[TipoNotificacion] = None
    prioridad: Optional[PrioridadNotificacion] = None
    estado: Optional[EstadoNotificacion] = None
    usuario_id: Optional[int] = None
    entidad_id: Optional[int] = None
    entidad_tipo: Optional[str] = None
    datos_adicionales: Optional[Dict[str, Any]] = None
    fecha_expiracion: Optional[datetime] = None
    accion_url: Optional[str] = None
    accion_texto: Optional[str] = None

class Notificacion(NotificacionBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    fecha_lectura: Optional[datetime] = None
    usuario_nombre: Optional[str] = None
    usuario_correo: Optional[str] = None
    usuario_rol: Optional[str] = None

    class Config:
        orm_mode = True

class NotificacionEstadisticas(BaseModel):
    total_notificaciones: int
    notificaciones_por_tipo: dict
    notificaciones_por_prioridad: dict
    notificaciones_por_estado: dict
    notificaciones_por_usuario: dict
    notificaciones_no_leidas: int
    notificaciones_urgentes: int
    promedio_tiempo_lectura: float  # en horas
    notificaciones_expiradas: int
