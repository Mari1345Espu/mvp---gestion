from pydantic import BaseModel
from datetime import datetime

class RecursoBase(BaseModel):
    proyecto_id: int
    descripcion: str
    cantidad: int
    fecha_solicitud: datetime
    fecha_respuesta: datetime
    estado_id: int
    tipo_estado_id: int

class RecursoCreate(RecursoBase):
    pass

class Recurso(RecursoBase):
    id: int

    class Config:
        orm_mode = True
