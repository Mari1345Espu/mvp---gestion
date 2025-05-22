from pydantic import BaseModel, EmailStr, constr
from typing import Optional, List
from datetime import datetime

class ParticipanteBase(BaseModel):
    nombre: constr(min_length=3, max_length=100)
    correo: EmailStr
    telefono: Optional[str] = None
    tipo: constr(min_length=3, max_length=50)  # Estudiante, Docente, Externo, etc.
    extension_id: int
    facultad_id: Optional[int] = None
    programa_id: Optional[int] = None
    rol: Optional[str] = None  # Rol en la extensión
    estado_id: Optional[int] = 1
    tipo_estado_id: Optional[int] = 1
    observaciones: Optional[str] = None
    documentos: Optional[List[str]] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    horas_participacion: Optional[int] = 0
    certificado: Optional[bool] = False
    notas: Optional[str] = None

class ParticipanteCreate(ParticipanteBase):
    pass

class ParticipanteUpdate(BaseModel):
    nombre: Optional[constr(min_length=3, max_length=100)] = None
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = None
    tipo: Optional[constr(min_length=3, max_length=50)] = None
    extension_id: Optional[int] = None
    facultad_id: Optional[int] = None
    programa_id: Optional[int] = None
    rol: Optional[str] = None
    estado_id: Optional[int] = None
    tipo_estado_id: Optional[int] = None
    observaciones: Optional[str] = None
    documentos: Optional[List[str]] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    horas_participacion: Optional[int] = None
    certificado: Optional[bool] = None
    notas: Optional[str] = None

class Participante(ParticipanteBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    extension_nombre: Optional[str] = None
    facultad_nombre: Optional[str] = None
    programa_nombre: Optional[str] = None
    estado_nombre: Optional[str] = None
    tipo_estado_nombre: Optional[str] = None

    class Config:
        orm_mode = True

class ParticipanteEstadisticas(BaseModel):
    total_participantes: int
    participantes_por_tipo: dict
    participantes_por_extension: dict
    participantes_por_facultad: dict
    participantes_por_programa: dict
    participantes_por_estado: dict
    participantes_por_rol: dict
    promedio_horas_participacion: float
    total_certificados: int
    total_documentos: int
