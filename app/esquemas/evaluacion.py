from pydantic import BaseModel, constr
from typing import Optional, List
from datetime import datetime

class EvaluacionBase(BaseModel):
    nombre: constr(min_length=3, max_length=100)
    descripcion: Optional[constr(min_length=10, max_length=500)] = None
    tipo_evaluacion: constr(min_length=3, max_length=50)
    entidad_id: int
    fecha_evaluacion: datetime
    estado_id: Optional[int] = 1
    tipo_estado_id: Optional[int] = 1
    responsable_id: int
    observaciones: Optional[str] = None
    documentos: Optional[List[str]] = None
    puntuacion: Optional[float] = None
    criterios: Optional[dict] = None
    recomendaciones: Optional[str] = None
    presupuesto_final: Optional[float] = None
    cumplimiento_objetivos: Optional[float] = None
    impacto: Optional[str] = None
    lecciones_aprendidas: Optional[str] = None

class EvaluacionCreate(EvaluacionBase):
    pass

class EvaluacionUpdate(BaseModel):
    nombre: Optional[constr(min_length=3, max_length=100)] = None
    descripcion: Optional[constr(min_length=10, max_length=500)] = None
    tipo_evaluacion: Optional[constr(min_length=3, max_length=50)] = None
    fecha_evaluacion: Optional[datetime] = None
    estado_id: Optional[int] = None
    tipo_estado_id: Optional[int] = None
    responsable_id: Optional[int] = None
    observaciones: Optional[str] = None
    documentos: Optional[List[str]] = None
    puntuacion: Optional[float] = None
    criterios: Optional[dict] = None
    recomendaciones: Optional[str] = None
    presupuesto_final: Optional[float] = None
    cumplimiento_objetivos: Optional[float] = None
    impacto: Optional[str] = None
    lecciones_aprendidas: Optional[str] = None

class Evaluacion(EvaluacionBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    entidad_nombre: Optional[str] = None
    estado_nombre: Optional[str] = None
    tipo_estado_nombre: Optional[str] = None
    responsable_nombre: Optional[str] = None
    responsable_correo: Optional[str] = None
    responsable_rol: Optional[str] = None

    class Config:
        orm_mode = True

class EvaluacionEstadisticas(BaseModel):
    total_evaluaciones: int
    evaluaciones_por_tipo: dict
    evaluaciones_por_estado: dict
    evaluaciones_por_responsable: dict
    evaluaciones_por_mes: dict
    evaluaciones_por_dia: dict
    evaluaciones_por_hora: dict
    promedio_puntuacion: float
    promedio_cumplimiento: float
    promedio_presupuesto: float
    total_documentos: int
    total_recomendaciones: int
    total_lecciones: int
