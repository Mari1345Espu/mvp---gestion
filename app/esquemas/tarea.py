from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TareaBase(BaseModel):
    cronograma_id: int
    nombre: str
    descripcion: str
    fecha_inicio: datetime
    fecha_fin: datetime
    estado_id: int
    tipo_estado_id: int
    aprobado: bool = False
    fecha_aprobacion: Optional[datetime] = None
    aprobado_por_id: Optional[int] = None
    observaciones: Optional[str] = None
    porcentaje_avance: float = 0
    fecha_ultimo_avance: Optional[datetime] = None
    responsable_id: Optional[int] = None

class TareaCreate(TareaBase):
    pass

class TareaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    estado_id: Optional[int] = None
    tipo_estado_id: Optional[int] = None
    aprobado: Optional[bool] = None
    fecha_aprobacion: Optional[datetime] = None
    aprobado_por_id: Optional[int] = None
    observaciones: Optional[str] = None
    porcentaje_avance: Optional[float] = None
    fecha_ultimo_avance: Optional[datetime] = None
    responsable_id: Optional[int] = None

class Tarea(TareaBase):
    id: int
    cronograma_nombre: Optional[str] = None
    estado_nombre: Optional[str] = None
    tipo_estado_nombre: Optional[str] = None
    aprobado_por_nombre: Optional[str] = None
    responsable_nombre: Optional[str] = None

    class Config:
        orm_mode = True
