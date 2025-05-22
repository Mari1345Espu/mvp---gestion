from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ConceptoEvaluacionBase(BaseModel):
    proyecto_id: int
    evaluador_id: int
    fecha_evaluacion: datetime
    puntaje: float
    observaciones: str
    recomendaciones: Optional[str] = None
    aprobado: bool = False
    estado_id: int
    tipo_estado_id: int
    criterio1_puntaje: Optional[float] = None
    criterio2_puntaje: Optional[float] = None
    criterio3_puntaje: Optional[float] = None
    criterio4_puntaje: Optional[float] = None
    criterio5_puntaje: Optional[float] = None

class ConceptoEvaluacionCreate(ConceptoEvaluacionBase):
    pass

class ConceptoEvaluacionUpdate(BaseModel):
    fecha_evaluacion: Optional[datetime] = None
    puntaje: Optional[float] = None
    observaciones: Optional[str] = None
    recomendaciones: Optional[str] = None
    aprobado: Optional[bool] = None
    estado_id: Optional[int] = None
    tipo_estado_id: Optional[int] = None
    criterio1_puntaje: Optional[float] = None
    criterio2_puntaje: Optional[float] = None
    criterio3_puntaje: Optional[float] = None
    criterio4_puntaje: Optional[float] = None
    criterio5_puntaje: Optional[float] = None

class ConceptoEvaluacion(ConceptoEvaluacionBase):
    id: int
    proyecto_titulo: Optional[str] = None
    evaluador_nombre: Optional[str] = None
    estado_nombre: Optional[str] = None
    tipo_estado_nombre: Optional[str] = None

    class Config:
        orm_mode = True
