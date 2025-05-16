from pydantic import BaseModel

class ProgramaBase(BaseModel):
    nombre: str
    descripcion: str
    facultad_id: int
    estado_id: int
    tipo_estado_id: int

class ProgramaCreate(ProgramaBase):
    pass

class Programa(ProgramaBase):
    id: int

    class Config:
        from_attributes = True
