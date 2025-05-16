from pydantic import BaseModel
from datetime import datetime

class ConvocatoriaBase(BaseModel):
    tipo: str
    fecha_inicio: datetime
    fecha_fin: datetime
    fecha_inicio_ejecucion: datetime
    fecha_fin_ejecucion: datetime
    estado_id: int
    tipo_estado_id: int

class ConvocatoriaCreate(ConvocatoriaBase):
    pass

class Convocatoria(ConvocatoriaBase):
    id: int

    class Config:
        from_attributes = True
