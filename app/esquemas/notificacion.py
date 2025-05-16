from pydantic import BaseModel
from datetime import datetime

class NotificacionBase(BaseModel):
    titulo: str
    mensaje: str
    fecha_envio: datetime
    usuario_id: int
    estado_id: int
    tipo_estado_id: int

class NotificacionCreate(NotificacionBase):
    pass

class Notificacion(NotificacionBase):
    id: int

    class Config:
        from_attributes = True
