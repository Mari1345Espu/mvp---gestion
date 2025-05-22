from pydantic import BaseModel, constr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class TipoSeguimiento(str, Enum):
    AVANCE = "avance"
    HITO = "hito"
    RIESGO = "riesgo"
    CAMBIO = "cambio"
    OBSERVACION = "observacion"

class EstadoSeguimiento(str, Enum):
    PENDIENTE = "pendiente"
    EN_PROCESO = "en_proceso"
    COMPLETADO = "completado"
    RETRASADO = "retrasado"
    CANCELADO = "cancelado"

class SeguimientoBase(BaseModel):
    titulo: constr(min_length=3, max_length=200)
    descripcion: constr(min_length=10, max_length=1000)
    tipo: TipoSeguimiento
    estado: EstadoSeguimiento = EstadoSeguimiento.PENDIENTE
    extension_id: int
    usuario_id: int
    fecha_limite: Optional[datetime] = None
    fecha_completado: Optional[datetime] = None
    porcentaje_avance: Optional[float] = None
    prioridad: Optional[int] = None
    impacto: Optional[str] = None
    acciones_tomadas: Optional[str] = None
    recursos_necesarios: Optional[str] = None
    observaciones: Optional[str] = None
    documentos: Optional[List[str]] = None
    etiquetas: Optional[List[str]] = None
    dependencias: Optional[List[int]] = None
    responsables: Optional[List[int]] = None
    datos_adicionales: Optional[Dict[str, Any]] = None

class SeguimientoCreate(SeguimientoBase):
    pass

class SeguimientoUpdate(BaseModel):
    titulo: Optional[constr(min_length=3, max_length=200)] = None
    descripcion: Optional[constr(min_length=10, max_length=1000)] = None
    tipo: Optional[TipoSeguimiento] = None
    estado: Optional[EstadoSeguimiento] = None
    fecha_limite: Optional[datetime] = None
    fecha_completado: Optional[datetime] = None
    porcentaje_avance: Optional[float] = None
    prioridad: Optional[int] = None
    impacto: Optional[str] = None
    acciones_tomadas: Optional[str] = None
    recursos_necesarios: Optional[str] = None
    observaciones: Optional[str] = None
    documentos: Optional[List[str]] = None
    etiquetas: Optional[List[str]] = None
    dependencias: Optional[List[int]] = None
    responsables: Optional[List[int]] = None
    datos_adicionales: Optional[Dict[str, Any]] = None

class Seguimiento(SeguimientoBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    extension_nombre: Optional[str] = None
    usuario_nombre: Optional[str] = None
    usuario_correo: Optional[str] = None
    usuario_rol: Optional[str] = None

    class Config:
        orm_mode = True

class SeguimientoEstadisticas(BaseModel):
    total_seguimientos: int
    seguimientos_por_tipo: dict
    seguimientos_por_estado: dict
    seguimientos_por_extension: dict
    seguimientos_por_usuario: dict
    seguimientos_pendientes: int
    seguimientos_en_proceso: int
    seguimientos_completados: int
    seguimientos_retrasados: int
    seguimientos_cancelados: int
    promedio_avance: float
    seguimientos_ultimo_mes: int
    seguimientos_por_prioridad: dict
    seguimientos_por_impacto: dict
