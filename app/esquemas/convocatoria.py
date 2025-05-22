from pydantic import BaseModel, constr
from typing import List, Optional
from datetime import datetime
from pydantic import EmailStr

class ConvocatoriaBase(BaseModel):
    nombre: constr(min_length=5, max_length=200)
    descripcion: constr(min_length=10)
    fecha_inicio: datetime
    fecha_fin: datetime
    estado_id: int
    tipo_estado_id: int
    tipo_proyecto_id: int
    presupuesto_total: Optional[float] = None
    presupuesto_por_proyecto: Optional[float] = None
    requisitos: Optional[str] = None
    criterios_evaluacion: Optional[str] = None
    documentos_requeridos: Optional[str] = None
    observaciones: Optional[str] = None
    url_bases: Optional[str] = None
    contacto_nombre: Optional[str] = None
    contacto_correo: Optional[EmailStr] = None
    contacto_telefono: Optional[str] = None

class ConvocatoriaCreate(ConvocatoriaBase):
    pass

class ConvocatoriaUpdate(BaseModel):
    nombre: Optional[constr(min_length=5, max_length=200)] = None
    descripcion: Optional[constr(min_length=10)] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    estado_id: Optional[int] = None
    tipo_estado_id: Optional[int] = None
    tipo_proyecto_id: Optional[int] = None
    presupuesto_total: Optional[float] = None
    presupuesto_por_proyecto: Optional[float] = None
    requisitos: Optional[str] = None
    criterios_evaluacion: Optional[str] = None
    documentos_requeridos: Optional[str] = None
    observaciones: Optional[str] = None
    url_bases: Optional[str] = None
    contacto_nombre: Optional[str] = None
    contacto_correo: Optional[EmailStr] = None
    contacto_telefono: Optional[str] = None

class Convocatoria(ConvocatoriaBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    estado_nombre: Optional[str] = None
    tipo_estado_nombre: Optional[str] = None
    tipo_proyecto_nombre: Optional[str] = None
    total_proyectos: Optional[int] = 0
    total_presupuesto_asignado: Optional[float] = 0
    proyectos_aprobados: Optional[int] = 0
    proyectos_rechazados: Optional[int] = 0
    proyectos_pendientes: Optional[int] = 0

    class Config:
        orm_mode = True

class ConvocatoriaEstadisticas(BaseModel):
    total_convocatorias: int
    convocatorias_por_estado: dict
    convocatorias_por_tipo_estado: dict
    convocatorias_por_tipo_proyecto: dict
    convocatorias_activas: int
    convocatorias_finalizadas: int
    convocatorias_por_mes: dict
    promedio_proyectos: float
    promedio_presupuesto: float
    total_presupuesto_asignado: float
    proyectos_por_convocatoria: dict
