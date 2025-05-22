from pydantic import BaseModel, constr
from typing import Optional, List
from datetime import datetime

class CronogramaBase(BaseModel):
    nombre: constr(min_length=3, max_length=200)
    descripcion: Optional[constr(min_length=10, max_length=500)] = None
    proyecto_id: int
    fecha_inicio: datetime
    fecha_fin: datetime
    estado_id: Optional[int] = 1
    tipo_estado_id: Optional[int] = 1
    observaciones: Optional[str] = None
    responsable_id: Optional[int] = None
    porcentaje_avance: Optional[float] = 0.0
    prioridad: Optional[int] = 1
    dependencias: Optional[List[int]] = None
    recursos_asignados: Optional[str] = None
    costo_estimado: Optional[float] = None
    costo_real: Optional[float] = None

class CronogramaCreate(CronogramaBase):
    pass

class CronogramaUpdate(BaseModel):
    nombre: Optional[constr(min_length=3, max_length=200)] = None
    descripcion: Optional[constr(min_length=10, max_length=500)] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    estado_id: Optional[int] = None
    tipo_estado_id: Optional[int] = None
    observaciones: Optional[str] = None
    responsable_id: Optional[int] = None
    porcentaje_avance: Optional[float] = None
    prioridad: Optional[int] = None
    dependencias: Optional[List[int]] = None
    recursos_asignados: Optional[str] = None
    costo_estimado: Optional[float] = None
    costo_real: Optional[float] = None

class Cronograma(CronogramaBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    proyecto_nombre: Optional[str] = None
    estado_nombre: Optional[str] = None
    tipo_estado_nombre: Optional[str] = None
    responsable_nombre: Optional[str] = None
    duracion_dias: Optional[int] = None
    dias_restantes: Optional[int] = None
    atraso_dias: Optional[int] = None
    dependencias_nombres: Optional[List[str]] = None

    class Config:
        orm_mode = True

class CronogramaEstadisticas(BaseModel):
    total_cronogramas: int
    cronogramas_por_estado: dict
    cronogramas_por_tipo_estado: dict
    cronogramas_por_proyecto: dict
    cronogramas_por_responsable: dict
    cronogramas_por_mes: dict
    cronogramas_atrasados: int
    cronogramas_completados: int
    cronogramas_en_progreso: int
    promedio_avance: float
    promedio_duracion: float
    promedio_atraso: float
    total_costo_estimado: float
    total_costo_real: float
    variacion_costo: float
