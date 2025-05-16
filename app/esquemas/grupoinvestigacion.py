from pydantic import BaseModel
from datetime import datetime

class GrupoInvestigacionBase(BaseModel):
    nombre: str
    descripcion: str
    fecha_creacion: datetime
    lider_id: int
    estado_id: int
    tipo_estado_id: int
    categoria: str
    categoria_minciencias: str

class GrupoInvestigacionCreate(GrupoInvestigacionBase):
    pass

class GrupoInvestigacion(GrupoInvestigacionBase):
    id: int

    class Config:
        from_attributes = True
