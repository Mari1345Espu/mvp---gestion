from pydantic import BaseModel, constr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class TipoReporte(str, Enum):
    EXTENSION = "extension"
    PARTICIPANTE = "participante"
    RECURSO = "recurso"
    FACULTAD = "facultad"
    PROGRAMA = "programa"
    GENERAL = "general"

class FormatoReporte(str, Enum):
    PDF = "pdf"
    EXCEL = "excel"
    CSV = "csv"

class EstadoReporte(str, Enum):
    PENDIENTE = "pendiente"
    PROCESANDO = "procesando"
    COMPLETADO = "completado"
    ERROR = "error"

class ReporteBase(BaseModel):
    titulo: constr(min_length=3, max_length=100)
    descripcion: Optional[str] = None
    tipo_reporte: str
    fecha_inicio: datetime
    fecha_fin: datetime
    estado_id: Optional[int] = 1
    tipo_estado_id: Optional[int] = 1
    observaciones: Optional[str] = None
    archivo_url: Optional[str] = None

class ReporteCreate(ReporteBase):
    pass

class ReporteUpdate(BaseModel):
    titulo: Optional[constr(min_length=3, max_length=100)] = None
    descripcion: Optional[str] = None
    tipo_reporte: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    estado_id: Optional[int] = None
    tipo_estado_id: Optional[int] = None
    observaciones: Optional[str] = None
    archivo_url: Optional[str] = None

class Reporte(ReporteBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    creado_por_id: int
    aprobado: bool
    fecha_aprobacion: Optional[datetime] = None
    aprobado_por_id: Optional[int] = None
    creado_por_nombre: Optional[str] = None
    aprobado_por_nombre: Optional[str] = None
    estado_nombre: Optional[str] = None
    tipo_estado_nombre: Optional[str] = None

    class Config:
        from_attributes = True

class ReporteEstadisticas(BaseModel):
    total_reportes: int
    reportes_por_tipo: dict
    reportes_por_formato: dict
    reportes_por_estado: dict
    reportes_por_usuario: dict
    reportes_pendientes: int
    reportes_procesando: int
    reportes_completados: int
    reportes_error: int
    promedio_tiempo_procesamiento: float  # en minutos
    reportes_ultimo_mes: int 