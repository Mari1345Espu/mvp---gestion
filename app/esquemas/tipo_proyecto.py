from pydantic import BaseModel

class TipoProyectoBase(BaseModel):
    nombre: str
    descripcion: str

class TipoProyectoCreate(TipoProyectoBase):
    pass

class TipoProyecto(TipoProyectoBase):
    id: int

    class Config:
        from_attributes = True
