from pydantic import BaseModel, constr, EmailStr
from typing import Optional, List
from datetime import datetime

class GrupoInvestigacionBase(BaseModel):
    nombre: constr(min_length=3, max_length=200)
    codigo: constr(min_length=3, max_length=50)
    descripcion: constr(min_length=10)
    fecha_creacion: datetime
    fecha_renovacion: Optional[datetime] = None
    fecha_vencimiento: Optional[datetime] = None
    estado_id: int
    tipo_estado_id: int
    director_id: int
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = None
    pagina_web: Optional[str] = None
    logo: Optional[str] = None
    lineas_investigacion: Optional[str] = None
    observaciones: Optional[str] = None

class GrupoInvestigacionCreate(GrupoInvestigacionBase):
    pass

class GrupoInvestigacionUpdate(BaseModel):
    nombre: Optional[constr(min_length=3, max_length=200)] = None
    codigo: Optional[constr(min_length=3, max_length=50)] = None
    descripcion: Optional[constr(min_length=10)] = None
    fecha_renovacion: Optional[datetime] = None
    fecha_vencimiento: Optional[datetime] = None
    estado_id: Optional[int] = None
    tipo_estado_id: Optional[int] = None
    director_id: Optional[int] = None
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = None
    pagina_web: Optional[str] = None
    logo: Optional[str] = None
    lineas_investigacion: Optional[str] = None
    observaciones: Optional[str] = None

class GrupoInvestigacion(GrupoInvestigacionBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    estado_nombre: Optional[str] = None
    tipo_estado_nombre: Optional[str] = None
    director_nombre: Optional[str] = None
    total_integrantes: Optional[int] = 0
    total_proyectos: Optional[int] = 0
    total_productos: Optional[int] = 0

    class Config:
        orm_mode = True

class GrupoInvestigacionEstadisticas(BaseModel):
    total_grupos: int
    grupos_por_estado: dict
    grupos_por_tipo_estado: dict
    grupos_activos: int
    grupos_vencidos: int
    grupos_por_mes: dict
    promedio_integrantes: float
    promedio_proyectos: float
    promedio_productos: float
    grupos_por_director: dict
