from pydantic import BaseModel, constr
from typing import Optional, List
from datetime import datetime

class FacultadBase(BaseModel):
    nombre: constr(min_length=3, max_length=100)
    descripcion: Optional[constr(min_length=10, max_length=500)] = None
    codigo: constr(min_length=2, max_length=20)
    estado_id: Optional[int] = 1
    tipo_estado_id: Optional[int] = 1
    responsable_id: int
    observaciones: Optional[str] = None
    documentos: Optional[List[str]] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

class FacultadCreate(FacultadBase):
    pass

class FacultadUpdate(BaseModel):
    nombre: Optional[constr(min_length=3, max_length=100)] = None
    descripcion: Optional[constr(min_length=10, max_length=500)] = None
    codigo: Optional[constr(min_length=2, max_length=20)] = None
    estado_id: Optional[int] = None
    tipo_estado_id: Optional[int] = None
    responsable_id: Optional[int] = None
    observaciones: Optional[str] = None
    documentos: Optional[List[str]] = None

class Facultad(FacultadBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    estado_nombre: Optional[str] = None
    tipo_estado_nombre: Optional[str] = None
    responsable_nombre: Optional[str] = None
    responsable_correo: Optional[str] = None
    responsable_rol: Optional[str] = None
    total_programas: Optional[int] = None
    total_extensiones: Optional[int] = None

    class Config:
        orm_mode = True

class FacultadEstadisticas(BaseModel):
    total_facultades: int
    facultades_por_estado: dict
    facultades_por_responsable: dict
    total_programas: int
    programas_por_facultad: dict
    total_extensiones: int
    extensiones_por_facultad: dict
    promedio_programas: float
    promedio_extensiones: float
    total_documentos: int
