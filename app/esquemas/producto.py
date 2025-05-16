from pydantic import BaseModel
from datetime import datetime

class ProductoBase(BaseModel):
    proyecto_id: int
    nombre: str
    descripcion: str
    fecha_creacion: datetime
    estado_id: int
    tipo_estado_id: int

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int

    class Config:
        orm_mode = True
