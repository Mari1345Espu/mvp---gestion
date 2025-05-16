from pydantic import BaseModel

class FacultadBase(BaseModel):
    nombre: str
    descripcion: str
    estado_id: int
    tipo_estado_id: int

class FacultadCreate(FacultadBase):
    pass

class Facultad(FacultadBase):
    id: int

    class Config:
        from_attributes = True
