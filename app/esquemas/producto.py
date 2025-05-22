from pydantic import BaseModel, constr
from typing import Optional, List
from datetime import datetime

class ProductoBase(BaseModel):
    titulo: constr(min_length=5, max_length=200)
    descripcion: constr(min_length=10)
    tipo_producto_id: int
    proyecto_id: int
    estado_id: int
    tipo_estado_id: int
    fecha_publicacion: Optional[datetime] = None
    fecha_aprobacion: Optional[datetime] = None
    aprobado_por_id: Optional[int] = None
    observaciones: Optional[str] = None
    url: Optional[str] = None
    doi: Optional[str] = None
    issn: Optional[str] = None
    isbn: Optional[str] = None
    revista: Optional[str] = None
    editorial: Optional[str] = None
    volumen: Optional[str] = None
    numero: Optional[str] = None
    pagina_inicio: Optional[int] = None
    pagina_fin: Optional[int] = None
    autores: Optional[str] = None
    palabras_clave: Optional[str] = None
    resumen: Optional[str] = None
    archivo: Optional[str] = None

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    titulo: Optional[constr(min_length=5, max_length=200)] = None
    descripcion: Optional[constr(min_length=10)] = None
    tipo_producto_id: Optional[int] = None
    estado_id: Optional[int] = None
    tipo_estado_id: Optional[int] = None
    fecha_publicacion: Optional[datetime] = None
    fecha_aprobacion: Optional[datetime] = None
    aprobado_por_id: Optional[int] = None
    observaciones: Optional[str] = None
    url: Optional[str] = None
    doi: Optional[str] = None
    issn: Optional[str] = None
    isbn: Optional[str] = None
    revista: Optional[str] = None
    editorial: Optional[str] = None
    volumen: Optional[str] = None
    numero: Optional[str] = None
    pagina_inicio: Optional[int] = None
    pagina_fin: Optional[int] = None
    autores: Optional[str] = None
    palabras_clave: Optional[str] = None
    resumen: Optional[str] = None
    archivo: Optional[str] = None

class Producto(ProductoBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    tipo_producto_nombre: Optional[str] = None
    proyecto_nombre: Optional[str] = None
    estado_nombre: Optional[str] = None
    tipo_estado_nombre: Optional[str] = None
    aprobado_por_nombre: Optional[str] = None

    class Config:
        orm_mode = True

class ProductoEstadisticas(BaseModel):
    total_productos: int
    productos_por_tipo: dict
    productos_por_estado: dict
    productos_por_proyecto: dict
    productos_aprobados: int
    productos_pendientes: int
    productos_rechazados: int
    promedio_tiempo_aprobacion: float
    productos_por_mes: dict
