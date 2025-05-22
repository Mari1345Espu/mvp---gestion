from pydantic import BaseModel, constr
from typing import Optional, List
from datetime import datetime

class ProgramaBase(BaseModel):
    nombre: constr(min_length=3, max_length=100)
    descripcion: Optional[constr(min_length=10, max_length=500)] = None
    codigo: constr(min_length=2, max_length=20)
    facultad_id: int
    estado_id: Optional[int] = 1
    tipo_estado_id: Optional[int] = 1
    responsable_id: int
    observaciones: Optional[str] = None
    documentos: Optional[List[str]] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    nivel: Optional[str] = None
    modalidad: Optional[str] = None
    duracion: Optional[int] = None
    creditos: Optional[int] = None
    resolucion: Optional[str] = None
    acreditacion: Optional[bool] = False
    fecha_acreditacion: Optional[datetime] = None
    vigencia_acreditacion: Optional[datetime] = None

class ProgramaCreate(ProgramaBase):
    pass

class ProgramaUpdate(BaseModel):
    nombre: Optional[constr(min_length=3, max_length=100)] = None
    descripcion: Optional[constr(min_length=10, max_length=500)] = None
    codigo: Optional[constr(min_length=2, max_length=20)] = None
    facultad_id: Optional[int] = None
    estado_id: Optional[int] = None
    tipo_estado_id: Optional[int] = None
    responsable_id: Optional[int] = None
    observaciones: Optional[str] = None
    documentos: Optional[List[str]] = None
    nivel: Optional[str] = None
    modalidad: Optional[str] = None
    duracion: Optional[int] = None
    creditos: Optional[int] = None
    resolucion: Optional[str] = None
    acreditacion: Optional[bool] = None
    fecha_acreditacion: Optional[datetime] = None
    vigencia_acreditacion: Optional[datetime] = None

class Programa(ProgramaBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    facultad_nombre: Optional[str] = None
    estado_nombre: Optional[str] = None
    tipo_estado_nombre: Optional[str] = None
    responsable_nombre: Optional[str] = None
    responsable_correo: Optional[str] = None
    responsable_rol: Optional[str] = None
    total_extensiones: Optional[int] = None

    class Config:
        orm_mode = True

class ProgramaEstadisticas(BaseModel):
    total_programas: int
    programas_por_facultad: dict
    programas_por_estado: dict
    programas_por_responsable: dict
    programas_por_nivel: dict
    programas_por_modalidad: dict
    programas_acreditados: int
    programas_no_acreditados: int
    total_extensiones: int
    extensiones_por_programa: dict
    promedio_extensiones: float
    promedio_duracion: float
    promedio_creditos: float
    total_documentos: int
