from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificacionBase(BaseModel):
    tipo: str
    mensaje: str
    proyecto_id: Optional[int] = None

class NotificacionCreate(NotificacionBase):
    usuario_id: int

class Notificacion(NotificacionBase):
    id: int
    usuario_id: int
    leida: bool
    fecha_creacion: datetime
    fecha_lectura: Optional[datetime] = None

    class Config:
        orm_mode = True

class NotificacionCount(BaseModel):
    count: int
