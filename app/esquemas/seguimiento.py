from pydantic import BaseModel
from datetime import datetime

class SeguimientoBase(BaseModel):
    fecha_seguimiento: datetime
    observaciones: str
    proyecto_id: int
    estado_id: int
    tipo_estado_id: int

class SeguimientoCreate(SeguimientoBase):
    pass

class Seguimiento(SeguimientoBase):
    id: int

    class Config:
        from_attributes = True
