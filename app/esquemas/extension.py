from pydantic import BaseModel, constr
from typing import Optional, List
from datetime import datetime

class ExtensionBase(BaseModel):
    nombre: constr(min_length=3, max_length=100)
    descripcion: Optional[constr(min_length=10, max_length=500)] = None
    codigo: constr(min_length=2, max_length=20)
    facultad_id: int
    programa_id: int
    estado_id: Optional[int] = 1
    tipo_estado_id: Optional[int] = 1
    responsable_id: int
    observaciones: Optional[str] = None
    documentos: Optional[List[str]] = None
    fecha_inicio: datetime
    fecha_fin: Optional[datetime] = None
    presupuesto: Optional[float] = None
    impacto: Optional[str] = None
    resultados: Optional[str] = None
    lecciones_aprendidas: Optional[str] = None

class ExtensionCreate(ExtensionBase):
    pass

class ExtensionUpdate(BaseModel):
    nombre: Optional[constr(min_length=3, max_length=100)] = None
    descripcion: Optional[constr(min_length=10, max_length=500)] = None
    codigo: Optional[constr(min_length=2, max_length=20)] = None
    facultad_id: Optional[int] = None
    programa_id: Optional[int] = None
    estado_id: Optional[int] = None
    tipo_estado_id: Optional[int] = None
    responsable_id: Optional[int] = None
    observaciones: Optional[str] = None
    documentos: Optional[List[str]] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    presupuesto: Optional[float] = None
    impacto: Optional[str] = None
    resultados: Optional[str] = None
    lecciones_aprendidas: Optional[str] = None

class Extension(ExtensionBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    facultad_nombre: Optional[str] = None
    programa_nombre: Optional[str] = None
    estado_nombre: Optional[str] = None
    tipo_estado_nombre: Optional[str] = None
    responsable_nombre: Optional[str] = None
    responsable_correo: Optional[str] = None
    responsable_rol: Optional[str] = None

    class Config:
        orm_mode = True

class ExtensionEstadisticas(BaseModel):
    total_extensiones: int
    extensiones_por_facultad: dict
    extensiones_por_programa: dict
    extensiones_por_estado: dict
    extensiones_por_responsable: dict
    extensiones_por_mes: dict
    extensiones_por_dia: dict
    extensiones_por_hora: dict
    promedio_presupuesto: float
    total_documentos: int
    total_resultados: int
    total_lecciones: int
