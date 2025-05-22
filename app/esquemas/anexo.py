from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime

class AnexoBase(BaseModel):
    nombre: constr(min_length=3, max_length=200)
    descripcion: Optional[constr(min_length=10, max_length=500)] = None
    tipo_anexo_id: int
    proyecto_id: Optional[int] = None
    producto_id: Optional[int] = None
    convocatoria_id: Optional[int] = None
    archivo: str
    estado_id: Optional[int] = 1
    tipo_estado_id: Optional[int] = 1
    observaciones: Optional[str] = None
    fecha_subida: Optional[datetime] = None
    subido_por_id: Optional[int] = None
    version: Optional[str] = None
    tamanio: Optional[int] = None
    tipo_archivo: Optional[str] = None

class AnexoCreate(AnexoBase):
    pass

class AnexoUpdate(BaseModel):
    nombre: Optional[constr(min_length=3, max_length=200)] = None
    descripcion: Optional[constr(min_length=10, max_length=500)] = None
    tipo_anexo_id: Optional[int] = None
    proyecto_id: Optional[int] = None
    producto_id: Optional[int] = None
    convocatoria_id: Optional[int] = None
    archivo: Optional[str] = None
    estado_id: Optional[int] = None
    tipo_estado_id: Optional[int] = None
    observaciones: Optional[str] = None
    version: Optional[str] = None
    tamanio: Optional[int] = None
    tipo_archivo: Optional[str] = None

class Anexo(AnexoBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    tipo_anexo_nombre: Optional[str] = None
    estado_nombre: Optional[str] = None
    tipo_estado_nombre: Optional[str] = None
    proyecto_nombre: Optional[str] = None
    producto_nombre: Optional[str] = None
    convocatoria_nombre: Optional[str] = None
    subido_por_nombre: Optional[str] = None

    class Config:
        orm_mode = True

class AnexoEstadisticas(BaseModel):
    total_anexos: int
    anexos_por_tipo: dict
    anexos_por_estado: dict
    anexos_por_tipo_estado: dict
    anexos_por_proyecto: dict
    anexos_por_producto: dict
    anexos_por_convocatoria: dict
    anexos_por_mes: dict
    promedio_tamanio: float
    total_espacio_ocupado: int
    anexos_por_tipo_archivo: dict
