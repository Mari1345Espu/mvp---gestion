from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ConvocatoriaBase(BaseModel):
    nombre: str
    descripcion: str
    fecha_inicio: datetime
    fecha_fin: datetime
    estado: str

class ConvocatoriaCreate(ConvocatoriaBase):
    pass

class ConvocatoriaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    estado: Optional[str] = None

class Convocatoria(ConvocatoriaBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True
