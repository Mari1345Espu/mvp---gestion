from pydantic import BaseModel

class ImpactoBase(BaseModel):
    nombre: str
    descripcion: str
    proyecto_id: int
    estado_id: int
    tipo_estado_id: int

class ImpactoCreate(ImpactoBase):
    pass

class Impacto(ImpactoBase):
    id: int

    class Config:
        from_attributes = True
