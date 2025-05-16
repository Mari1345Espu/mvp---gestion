from pydantic import BaseModel
from datetime import datetime

class ParticipanteBase(BaseModel):
    proyecto_id: int
    fecha_vinculacion: datetime
    nombre: str
    rol_id: int
    facultad_id: int
    programa_id: int
    estado_id: int
    tipo_estado_id: int

class ParticipanteCreate(ParticipanteBase):
    pass

class Participante(ParticipanteBase):
    id: int

    class Config:
        orm_mode = True
