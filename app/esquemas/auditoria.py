from pydantic import BaseModel, constr
from typing import Optional, Dict, Any
from datetime import datetime

class AuditoriaBase(BaseModel):
    usuario_id: int
    accion: constr(min_length=3, max_length=50)
    tabla: constr(min_length=3, max_length=50)
    registro_id: int
    datos_anteriores: Optional[Dict[str, Any]] = None
    datos_nuevos: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    observaciones: Optional[str] = None

class AuditoriaCreate(AuditoriaBase):
    pass

class Auditoria(AuditoriaBase):
    id: int
    fecha_creacion: datetime
    usuario_nombre: Optional[str] = None
    usuario_correo: Optional[str] = None
    usuario_rol: Optional[str] = None

    class Config:
        orm_mode = True

class AuditoriaEstadisticas(BaseModel):
    total_registros: int
    registros_por_accion: dict
    registros_por_tabla: dict
    registros_por_usuario: dict
    registros_por_mes: dict
    registros_por_dia: dict
    registros_por_hora: dict
    ultimas_acciones: list
    usuarios_mas_activos: dict
    tablas_mas_modificadas: dict
