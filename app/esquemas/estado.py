from pydantic import BaseModel

class EstadoBase(BaseModel):
    nombre: str
    tipo: str

class EstadoCreate(EstadoBase):
    pass

class Estado(EstadoBase):
    id: int

    class Config:
        orm_mode = True
