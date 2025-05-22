from pydantic import BaseModel, constr
from typing import Optional, List
from datetime import datetime

class TipoEstadoBase(BaseModel):
    nombre: constr(min_length=3, max_length=100)
    descripcion: Optional[constr(min_length=10, max_length=500)] = None
    codigo: constr(min_length=2, max_length=20)
    activo: Optional[bool] = True

class TipoEstadoCreate(TipoEstadoBase):
    pass

class TipoEstadoUpdate(BaseModel):
    nombre: Optional[constr(min_length=3, max_length=100)] = None
    descripcion: Optional[constr(min_length=10, max_length=500)] = None
    codigo: Optional[constr(min_length=2, max_length=20)] = None
    activo: Optional[bool] = None

class TipoEstado(TipoEstadoBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    total_estados: Optional[int] = None
    total_entidades: Optional[int] = None

    class Config:
        orm_mode = True

class TipoEstadoEstadisticas(BaseModel):
    total_tipos: int
    tipos_activos: int
    tipos_inactivos: int
    total_estados: int
    estados_por_tipo: dict
    total_entidades: int
    entidades_por_tipo: dict
