from pydantic import BaseModel
from datetime import datetime

class EvaluacionBase(BaseModel):
    nombre: str
    descripcion: str
    fecha_evaluacion: datetime
    proyecto_id: int
    estado_id: int
    tipo_estado_id: int

class EvaluacionCreate(EvaluacionBase):
    pass

class Evaluacion(EvaluacionBase):
    id: int

    class Config:
        from_attributes = True
