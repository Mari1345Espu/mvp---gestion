from pydantic import BaseModel
from datetime import datetime

class AuditoriaBase(BaseModel):
    accion: str
    tabla_afectada: str
    registro_id: int
    usuario_id: int
    fecha_accion: datetime
    estado_id: int
    tipo_estado_id: int

class AuditoriaCreate(AuditoriaBase):
    pass

class Auditoria(AuditoriaBase):
    id: int

    class Config:
        from_attributes = True
