from pydantic import BaseModel
from datetime import datetime

class AvanceBase(BaseModel):
    proyecto_id: int
    fecha_avance: datetime
    descripcion: str
    estado_id: int
    tipo_estado_id: int

class AvanceCreate(AvanceBase):
    pass

class Avance(AvanceBase):
    id: int

    class Config:
        orm_mode = True
