from pydantic import BaseModel, constr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class TipoImpacto(str, Enum):
    SOCIAL = "social"
    ECONOMICO = "economico"
    AMBIENTAL = "ambiental"
    CULTURAL = "cultural"
    EDUCATIVO = "educativo"
    TECNOLOGICO = "tecnologico"
    INSTITUCIONAL = "institucional"

class NivelImpacto(str, Enum):
    BAJO = "bajo"
    MEDIO = "medio"
    ALTO = "alto"
    MUY_ALTO = "muy_alto"

class ImpactoBase(BaseModel):
    titulo: constr(min_length=3, max_length=200)
    descripcion: constr(min_length=10, max_length=1000)
    tipo: TipoImpacto
    nivel: NivelImpacto
    extension_id: int
    usuario_id: int
    fecha_impacto: datetime
    beneficiarios_directos: Optional[int] = None
    beneficiarios_indirectos: Optional[int] = None
    indicadores: Optional[Dict[str, Any]] = None
    resultados: Optional[str] = None
    evidencias: Optional[List[str]] = None
    sostenibilidad: Optional[str] = None
    replicabilidad: Optional[str] = None
    observaciones: Optional[str] = None
    documentos: Optional[List[str]] = None
    datos_adicionales: Optional[Dict[str, Any]] = None

class ImpactoCreate(ImpactoBase):
    pass

class ImpactoUpdate(BaseModel):
    titulo: Optional[constr(min_length=3, max_length=200)] = None
    descripcion: Optional[constr(min_length=10, max_length=1000)] = None
    tipo: Optional[TipoImpacto] = None
    nivel: Optional[NivelImpacto] = None
    fecha_impacto: Optional[datetime] = None
    beneficiarios_directos: Optional[int] = None
    beneficiarios_indirectos: Optional[int] = None
    indicadores: Optional[Dict[str, Any]] = None
    resultados: Optional[str] = None
    evidencias: Optional[List[str]] = None
    sostenibilidad: Optional[str] = None
    replicabilidad: Optional[str] = None
    observaciones: Optional[str] = None
    documentos: Optional[List[str]] = None
    datos_adicionales: Optional[Dict[str, Any]] = None

class Impacto(ImpactoBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    extension_nombre: Optional[str] = None
    usuario_nombre: Optional[str] = None
    usuario_correo: Optional[str] = None
    usuario_rol: Optional[str] = None

    class Config:
        orm_mode = True

class ImpactoEstadisticas(BaseModel):
    total_impactos: int
    impactos_por_tipo: dict
    impactos_por_nivel: dict
    impactos_por_extension: dict
    impactos_por_usuario: dict
    total_beneficiarios_directos: int
    total_beneficiarios_indirectos: int
    promedio_beneficiarios: float
    impactos_ultimo_mes: int
    impactos_por_sostenibilidad: dict
    impactos_por_replicabilidad: dict
