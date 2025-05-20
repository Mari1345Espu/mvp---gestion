from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

class ProyectoBase(BaseModel):
    nombre: str
    descripcion: str
    fecha_inicio: datetime
    fecha_fin: datetime
    presupuesto: float
    estado_id: int
    facultad_id: int
    convocatoria_id: Optional[int] = None

class ProyectoCreate(ProyectoBase):
    pass

class ProyectoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    presupuesto: Optional[float] = None
    estado_id: Optional[int] = None
    facultad_id: Optional[int] = None
    convocatoria_id: Optional[int] = None

class Proyecto(ProyectoBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    avance: float = 0.0

    class Config:
        from_attributes = True

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
        from_attributes = True
