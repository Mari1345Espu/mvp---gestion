from pydantic import BaseModel

class TipoEstadoBase(BaseModel):
    nombre: str

class TipoEstadoCreate(TipoEstadoBase):
    pass

class TipoEstado(TipoEstadoBase):
    id: int

    class Config:
        from_attributes = True  # Cambiado de orm_mode a from_attributes
