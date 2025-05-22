from pydantic import BaseModel, constr
from typing import Optional, List
from datetime import datetime

class RolBase(BaseModel):
    nombre: constr(min_length=3, max_length=50)
    descripcion: Optional[constr(min_length=10, max_length=200)] = None
    permisos: Optional[List[str]] = None
    estado_id: Optional[int] = 1
    tipo_estado_id: Optional[int] = 1

class RolCreate(RolBase):
    pass

class RolUpdate(BaseModel):
    nombre: Optional[constr(min_length=3, max_length=50)] = None
    descripcion: Optional[constr(min_length=10, max_length=200)] = None
    permisos: Optional[List[str]] = None
    estado_id: Optional[int] = None
    tipo_estado_id: Optional[int] = None

class Rol(RolBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    estado_nombre: Optional[str] = None
    tipo_estado_nombre: Optional[str] = None
    total_usuarios: Optional[int] = 0

    class Config:
        orm_mode = True

class RolEstadisticas(BaseModel):
    total_roles: int
    roles_por_estado: dict
    roles_por_tipo_estado: dict
    roles_activos: int
    roles_inactivos: int
    roles_por_mes: dict
    promedio_usuarios: float
    roles_por_permiso: dict
