from pydantic import BaseModel

class DestinoBase(BaseModel):
    nombre: str
    descripcion: str
    proyecto_id: int
    estado_id: int
    tipo_estado_id: int

class DestinoCreate(DestinoBase):
    pass

class Destino(DestinoBase):
    id: int

    class Config:
        from_attributes = True
