from pydantic import BaseModel
from datetime import datetime

class ExtensionBase(BaseModel):
    nombre: str
    descripcion: str
    fecha_inicio: datetime
    fecha_fin: datetime
    proyecto_id: int
    estado_id: int
    tipo_estado_id: int

class ExtensionCreate(ExtensionBase):
    pass

class Extension(ExtensionBase):
    id: int

    class Config:
        from_attributes = True
