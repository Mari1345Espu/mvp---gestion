from pydantic import BaseModel
from datetime import datetime

class CierreBase(BaseModel):
    fecha_cierre: datetime
    observaciones: str
    proyecto_id: int
    estado_id: int
    tipo_estado_id: int

class CierreCreate(CierreBase):
    pass

class Cierre(CierreBase):
    id: int

    class Config:
        from_attributes = True
