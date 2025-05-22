from pydantic import BaseModel, constr
from typing import Optional, List
from datetime import datetime

class TipoProyectoBase(BaseModel):
    nombre: constr(min_length=3, max_length=100)
    descripcion: constr(min_length=10, max_length=500)
    codigo: constr(min_length=2, max_length=10)
    estado_id: Optional[int] = 1
    tipo_estado_id: Optional[int] = 1
    observaciones: Optional[str] = None
    documentos: Optional[List[str]] = None

class TipoProyectoCreate(TipoProyectoBase):
    pass

class TipoProyectoUpdate(BaseModel):
    nombre: Optional[constr(min_length=3, max_length=100)] = None
    descripcion: Optional[constr(min_length=10, max_length=500)] = None
    codigo: Optional[constr(min_length=2, max_length=10)] = None
    estado_id: Optional[int] = None
    tipo_estado_id: Optional[int] = None
    observaciones: Optional[str] = None
    documentos: Optional[List[str]] = None

class TipoProyecto(TipoProyectoBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    estado_nombre: Optional[str] = None
    tipo_estado_nombre: Optional[str] = None

    class Config:
        orm_mode = True

class TipoProyectoEstadisticas(BaseModel):
    total_tipos: int
    tipos_por_estado: dict
    tipos_por_tipo_estado: dict
    total_proyectos: int
    proyectos_por_tipo: dict
    promedio_proyectos_por_tipo: float
