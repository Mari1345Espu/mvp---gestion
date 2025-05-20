from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

class ProyectoBase(BaseModel):
    titulo: str
    objetivos: str
    convocatoria_id: int
    grupo_investigacion_id: int
    linea_investigacion_id: int
    extension_id: int
    estado_id: int
    fecha_inicio: datetime
    tipo_estado_id: int
    resumen: str
    evaluador_externo_id: int
    concepto_evaluacion_id: int
    cierre_id: int
    problematica: str

class ProyectoCreate(ProyectoBase):
    pass

class Proyecto(ProyectoBase):
    id: int

    class Config:
        orm_mode = True

class DashboardResponse(BaseModel):
    total_proyectos: int
    proyectos_por_estado: Dict[str, int]
    proyectos_por_vencer: int
    presupuesto_total: float
    gasto_total: float
    productos_por_tipo: Dict[str, int]
    proyectos_por_facultad: Dict[str, int]

class ReporteProyecto(BaseModel):
    total_proyectos: int
    presupuesto_total: float
    gasto_total: float
    avance_promedio: float
    proyectos: List[Proyecto]

    class Config:
        orm_mode = True
