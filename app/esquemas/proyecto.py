from pydantic import BaseModel, constr
from typing import List, Optional, Dict
from datetime import datetime, date

class ProyectoBase(BaseModel):
    titulo: constr(min_length=5, max_length=200)
    objetivos: constr(min_length=10)
    convocatoria_id: int
    grupo_investigacion_id: int
    linea_investigacion_id: int
    extension_id: int
    estado_id: int
    tipo_estado_id: int
    fecha_inicio: datetime
    evaluador_externo_id: Optional[int] = None
    asesor_id: Optional[int] = None
    fecha_fin: Optional[datetime] = None
    presupuesto: Optional[float] = None
    observaciones: Optional[str] = None
    palabras_clave: Optional[str] = None
    resumen: Optional[str] = None
    justificacion: Optional[str] = None
    metodologia: Optional[str] = None
    resultados_esperados: Optional[str] = None
    impacto_esperado: Optional[str] = None
    cronograma: Optional[str] = None
    recursos_necesarios: Optional[str] = None

class ProyectoCreate(ProyectoBase):
    pass

class ProyectoUpdate(BaseModel):
    titulo: Optional[constr(min_length=5, max_length=200)] = None
    objetivos: Optional[constr(min_length=10)] = None
    convocatoria_id: Optional[int] = None
    grupo_investigacion_id: Optional[int] = None
    linea_investigacion_id: Optional[int] = None
    extension_id: Optional[int] = None
    estado_id: Optional[int] = None
    tipo_estado_id: Optional[int] = None
    fecha_inicio: Optional[datetime] = None
    evaluador_externo_id: Optional[int] = None
    asesor_id: Optional[int] = None
    fecha_fin: Optional[datetime] = None
    presupuesto: Optional[float] = None
    observaciones: Optional[str] = None
    palabras_clave: Optional[str] = None
    resumen: Optional[str] = None
    justificacion: Optional[str] = None
    metodologia: Optional[str] = None
    resultados_esperados: Optional[str] = None
    impacto_esperado: Optional[str] = None
    cronograma: Optional[str] = None
    recursos_necesarios: Optional[str] = None

class Proyecto(ProyectoBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    convocatoria_nombre: Optional[str] = None
    grupo_investigacion_nombre: Optional[str] = None
    linea_investigacion_nombre: Optional[str] = None
    extension_nombre: Optional[str] = None
    estado_nombre: Optional[str] = None
    tipo_estado_nombre: Optional[str] = None
    evaluador_externo_nombre: Optional[str] = None
    asesor_nombre: Optional[str] = None
    porcentaje_avance: Optional[float] = 0
    productos_count: Optional[int] = 0
    avances_count: Optional[int] = 0
    recursos_count: Optional[int] = 0

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
        from_attributes = True

class ProyectoFiltro(BaseModel):
    convocatoria_id: Optional[int] = None
    estado_id: Optional[int] = None
    tipo_proyecto_id: Optional[int] = None
    programa_id: Optional[int] = None
    extension_id: Optional[int] = None

class ProyectoEstadisticas(BaseModel):
    total_proyectos: int
    proyectos_activos: int
    proyectos_finalizados: int
    proyectos_por_estado: dict
    proyectos_por_grupo: dict
    proyectos_por_linea: dict
    promedio_avance: float
    total_presupuesto: float
    presupuesto_por_grupo: dict
