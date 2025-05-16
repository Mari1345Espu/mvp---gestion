from pydantic import BaseModel
from datetime import datetime

class AnexoBase(BaseModel):
    nombre: str
    ruta_archivo: str
    fecha_subida: datetime
    proyecto_id: int
    estado_id: int
    tipo_estado_id: int

class AnexoCreate(AnexoBase):
    pass

class Anexo(AnexoBase):
    id: int

    class Config:
        from_attributes = True
