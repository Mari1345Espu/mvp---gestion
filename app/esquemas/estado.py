from pydantic import BaseModel, constr
from typing import Optional, List
from datetime import datetime

class EstadoBase(BaseModel):
    nombre: constr(min_length=3, max_length=100)
    descripcion: Optional[constr(min_length=10, max_length=500)] = None
    tipo_estado_id: int
    color: Optional[str] = None
    icono: Optional[str] = None
    orden: Optional[int] = 0
    activo: Optional[bool] = True

class EstadoCreate(EstadoBase):
    pass

class EstadoUpdate(BaseModel):
    nombre: Optional[constr(min_length=3, max_length=100)] = None
    descripcion: Optional[constr(min_length=10, max_length=500)] = None
    tipo_estado_id: Optional[int] = None
    color: Optional[str] = None
    icono: Optional[str] = None
    orden: Optional[int] = None
    activo: Optional[bool] = None

class Estado(EstadoBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    tipo_estado_nombre: Optional[str] = None
    total_entidades: Optional[int] = None

    class Config:
        orm_mode = True

class EstadoEstadisticas(BaseModel):
    total_estados: int
    estados_por_tipo: dict
    estados_activos: int
    estados_inactivos: int
    estados_por_orden: dict
    total_entidades: int
    entidades_por_estado: dict
