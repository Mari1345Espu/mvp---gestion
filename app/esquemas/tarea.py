from pydantic import BaseModel
from datetime import datetime

class TareaBase(BaseModel):
    cronograma_id: int
    nombre: str
    descripcion: str
    fecha_inicio: datetime
    fecha_fin: datetime
    estado_id: int
    tipo_estado_id: int

class TareaCreate(TareaBase):
    pass

class Tarea(TareaBase):
    id: int

    class Config:
        orm_mode = True
