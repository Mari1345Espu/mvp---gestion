from pydantic import BaseModel, constr
from typing import Optional, List, Dict, Any
from datetime import datetime

class DestinoBase(BaseModel):
    nombre: constr(min_length=3, max_length=200)
    descripcion: Optional[constr(min_length=10, max_length=500)] = None
    tipo_destino: constr(min_length=3, max_length=50)  # "proyecto" o "convocatoria"
    entidad_id: int  # ID del proyecto o convocatoria
    fecha_destino: datetime
    estado_id: Optional[int] = 1
    tipo_estado_id: Optional[int] = 1
    responsable_id: int
    observaciones: Optional[str] = None
    documentos: Optional[List[str]] = None
    evaluacion: Optional[Dict[str, Any]] = None
    recomendaciones: Optional[str] = None
    presupuesto_final: Optional[float] = None
    cumplimiento_objetivos: Optional[float] = None
    impacto: Optional[str] = None
    lecciones_aprendidas: Optional[str] = None

class DestinoCreate(DestinoBase):
    pass

class DestinoUpdate(BaseModel):
    nombre: Optional[constr(min_length=3, max_length=200)] = None
    descripcion: Optional[constr(min_length=10, max_length=500)] = None
    fecha_destino: Optional[datetime] = None
    estado_id: Optional[int] = None
    tipo_estado_id: Optional[int] = None
    responsable_id: Optional[int] = None
    observaciones: Optional[str] = None
    documentos: Optional[List[str]] = None
    evaluacion: Optional[Dict[str, Any]] = None
    recomendaciones: Optional[str] = None
    presupuesto_final: Optional[float] = None
    cumplimiento_objetivos: Optional[float] = None
    impacto: Optional[str] = None
    lecciones_aprendidas: Optional[str] = None

class Destino(DestinoBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    entidad_nombre: Optional[str] = None
    estado_nombre: Optional[str] = None
    tipo_estado_nombre: Optional[str] = None
    responsable_nombre: Optional[str] = None
    dias_desde_destino: Optional[int] = None
    total_documentos: Optional[int] = None
    evaluacion_promedio: Optional[float] = None

    class Config:
        orm_mode = True

class DestinoEstadisticas(BaseModel):
    total_destinos: int
    destinos_por_tipo: dict
    destinos_por_estado: dict
    destinos_por_responsable: dict
    destinos_por_mes: dict
    promedio_cumplimiento: float
    promedio_presupuesto_final: float
    total_presupuesto_final: float
    destinos_pendientes: int
    destinos_completados: int
    destinos_en_proceso: int
    evaluaciones_promedio: dict
    impactos_mas_comunes: dict
    lecciones_aprendidas: list
