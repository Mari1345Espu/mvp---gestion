from pydantic import BaseModel, constr
from typing import Optional, List
from datetime import datetime

class RecursoBase(BaseModel):
    nombre: constr(min_length=3, max_length=100)
    descripcion: Optional[constr(min_length=10, max_length=500)] = None
    codigo: constr(min_length=2, max_length=20)
    tipo: constr(min_length=3, max_length=50)
    facultad_id: int
    programa_id: Optional[int] = None
    extension_id: Optional[int] = None
    estado_id: Optional[int] = 1
    tipo_estado_id: Optional[int] = 1
    responsable_id: int
    observaciones: Optional[str] = None
    documentos: Optional[List[str]] = None
    fecha_adquisicion: Optional[datetime] = None
    fecha_vencimiento: Optional[datetime] = None
    valor: Optional[float] = None
    ubicacion: Optional[str] = None
    cantidad: Optional[int] = 1
    unidad_medida: Optional[str] = None
    proveedor: Optional[str] = None
    garantia: Optional[str] = None
    mantenimiento: Optional[str] = None
    estado_fisico: Optional[str] = None
    estado_operativo: Optional[str] = None
    fecha_ultimo_mantenimiento: Optional[datetime] = None
    fecha_proximo_mantenimiento: Optional[datetime] = None
    costo_mantenimiento: Optional[float] = None
    vida_util: Optional[int] = None
    depreciacion: Optional[float] = None
    seguro: Optional[str] = None
    poliza_seguro: Optional[str] = None
    fecha_vencimiento_seguro: Optional[datetime] = None
    costo_seguro: Optional[float] = None
    notas: Optional[str] = None

class RecursoCreate(RecursoBase):
    pass

class RecursoUpdate(BaseModel):
    nombre: Optional[constr(min_length=3, max_length=100)] = None
    descripcion: Optional[constr(min_length=10, max_length=500)] = None
    codigo: Optional[constr(min_length=2, max_length=20)] = None
    tipo: Optional[constr(min_length=3, max_length=50)] = None
    facultad_id: Optional[int] = None
    programa_id: Optional[int] = None
    extension_id: Optional[int] = None
    estado_id: Optional[int] = None
    tipo_estado_id: Optional[int] = None
    responsable_id: Optional[int] = None
    observaciones: Optional[str] = None
    documentos: Optional[List[str]] = None
    fecha_adquisicion: Optional[datetime] = None
    fecha_vencimiento: Optional[datetime] = None
    valor: Optional[float] = None
    ubicacion: Optional[str] = None
    cantidad: Optional[int] = None
    unidad_medida: Optional[str] = None
    proveedor: Optional[str] = None
    garantia: Optional[str] = None
    mantenimiento: Optional[str] = None
    estado_fisico: Optional[str] = None
    estado_operativo: Optional[str] = None
    fecha_ultimo_mantenimiento: Optional[datetime] = None
    fecha_proximo_mantenimiento: Optional[datetime] = None
    costo_mantenimiento: Optional[float] = None
    vida_util: Optional[int] = None
    depreciacion: Optional[float] = None
    seguro: Optional[str] = None
    poliza_seguro: Optional[str] = None
    fecha_vencimiento_seguro: Optional[datetime] = None
    costo_seguro: Optional[float] = None
    notas: Optional[str] = None

class Recurso(RecursoBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    facultad_nombre: Optional[str] = None
    programa_nombre: Optional[str] = None
    extension_nombre: Optional[str] = None
    estado_nombre: Optional[str] = None
    tipo_estado_nombre: Optional[str] = None
    responsable_nombre: Optional[str] = None
    responsable_correo: Optional[str] = None
    responsable_rol: Optional[str] = None

    class Config:
        orm_mode = True

class RecursoEstadisticas(BaseModel):
    total_recursos: int
    recursos_por_tipo: dict
    recursos_por_facultad: dict
    recursos_por_programa: dict
    recursos_por_extension: dict
    recursos_por_estado: dict
    recursos_por_responsable: dict
    promedio_valor: float
    total_documentos: int
