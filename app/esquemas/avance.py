from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AvanceBase(BaseModel):
    proyecto_id: int
    tarea_id: Optional[int] = None
    descripcion: str
    fecha_creacion: datetime
    estado_id: int
    tipo_estado_id: int
    aprobado: bool = False
    fecha_aprobacion: Optional[datetime] = None
    observaciones: Optional[str] = None
    aprobado_por_id: Optional[int] = None
    evidencias: Optional[str] = None
    porcentaje_completado: float = 0

class AvanceCreate(AvanceBase):
    pass

class AvanceUpdate(BaseModel):
    descripcion: Optional[str] = None
    estado_id: Optional[int] = None
    tipo_estado_id: Optional[int] = None
    aprobado: Optional[bool] = None
    fecha_aprobacion: Optional[datetime] = None
    observaciones: Optional[str] = None
    aprobado_por_id: Optional[int] = None
    evidencias: Optional[str] = None
    porcentaje_completado: Optional[float] = None

class Avance(AvanceBase):
    id: int
    proyecto_titulo: Optional[str] = None
    tarea_nombre: Optional[str] = None
    estado_nombre: Optional[str] = None
    tipo_estado_nombre: Optional[str] = None
    aprobado_por_nombre: Optional[str] = None

    class Config:
        orm_mode = True
