from pydantic import BaseModel, constr
from typing import Optional, List
from datetime import datetime

class LineaInvestigacionBase(BaseModel):
    nombre: constr(min_length=3, max_length=200)
    descripcion: constr(min_length=10)
    grupo_investigacion_id: int
    estado_id: int
    tipo_estado_id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    observaciones: Optional[str] = None
    objetivos: Optional[str] = None
    metodologia: Optional[str] = None
    resultados_esperados: Optional[str] = None
    recursos_necesarios: Optional[str] = None
    coordinador_id: Optional[int] = None

class LineaInvestigacionCreate(LineaInvestigacionBase):
    pass

class LineaInvestigacionUpdate(BaseModel):
    nombre: Optional[constr(min_length=3, max_length=200)] = None
    descripcion: Optional[constr(min_length=10)] = None
    estado_id: Optional[int] = None
    tipo_estado_id: Optional[int] = None
    observaciones: Optional[str] = None
    objetivos: Optional[str] = None
    metodologia: Optional[str] = None
    resultados_esperados: Optional[str] = None
    recursos_necesarios: Optional[str] = None
    coordinador_id: Optional[int] = None

class LineaInvestigacion(LineaInvestigacionBase):
    id: int
    grupo_nombre: Optional[str] = None
    estado_nombre: Optional[str] = None
    tipo_estado_nombre: Optional[str] = None
    coordinador_nombre: Optional[str] = None
    total_proyectos: Optional[int] = 0
    total_productos: Optional[int] = 0
    total_investigadores: Optional[int] = 0

    class Config:
        orm_mode = True

class LineaInvestigacionEstadisticas(BaseModel):
    total_lineas: int
    lineas_por_estado: dict
    lineas_por_tipo_estado: dict
    lineas_por_grupo: dict
    lineas_activas: int
    lineas_inactivas: int
    lineas_por_mes: dict
    promedio_proyectos: float
    promedio_productos: float
    promedio_investigadores: float
    lineas_por_coordinador: dict

