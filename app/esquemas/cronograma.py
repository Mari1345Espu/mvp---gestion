from pydantic import BaseModel
from datetime import datetime

class CronogramaBase(BaseModel):
    proyecto_id: int
    fecha_creacion: datetime
    estado_id: int
    tipo_estado_id: int

class CronogramaCreate(CronogramaBase):
    pass

class Cronograma(CronogramaBase):
    id: int

    class Config:
        orm_mode = True
