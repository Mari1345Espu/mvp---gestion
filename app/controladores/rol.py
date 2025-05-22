from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional
from datetime import datetime

from app import modelos
from app.db.session import get_db
from app.esquemas.rol import (
    Rol as RolSchema,
    RolCreate,
    RolUpdate,
    RolEstadisticas
)
from app.core.seguridad import get_current_user

router = APIRouter(
    prefix="/roles",
    tags=["roles"]
)

@router.get("/", response_model=List[RolSchema])
def read_roles(
    skip: int = 0,
    limit: int = 100,
    estado_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden ver los roles"
        )
    
    query = db.query(modelos.Rol)
    
    if estado_id:
        query = query.filter(modelos.Rol.estado_id == estado_id)
    if search:
        query = query.filter(
            or_(
                modelos.Rol.nombre.ilike(f"%{search}%"),
                modelos.Rol.descripcion.ilike(f"%{search}%")
            )
        )
    
    roles = query.offset(skip).limit(limit).all()
    return roles

@router.get("/{rol_id}", response_model=RolSchema)
def read_rol(
    rol_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden ver los roles"
        )
    
    rol = db.query(modelos.Rol).filter(modelos.Rol.id == rol_id).first()
    if rol is None:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol

@router.post("/", response_model=RolSchema)
def create_rol(
    rol: RolCreate,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden crear roles"
        )
    
    # Verificar que el nombre no esté duplicado
    existing_rol = db.query(modelos.Rol).filter(modelos.Rol.nombre == rol.nombre).first()
    if existing_rol:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un rol con ese nombre"
        )
    
    db_rol = modelos.Rol(**rol.dict())
    db.add(db_rol)
    db.commit()
    db.refresh(db_rol)
    return db_rol

@router.put("/{rol_id}", response_model=RolSchema)
def update_rol(
    rol_id: int,
    rol: RolUpdate,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden actualizar roles"
        )
    
    db_rol = db.query(modelos.Rol).filter(modelos.Rol.id == rol_id).first()
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    
    # Verificar que el nuevo nombre no esté duplicado si se está actualizando
    if rol.nombre and rol.nombre != db_rol.nombre:
        existing_rol = db.query(modelos.Rol).filter(modelos.Rol.nombre == rol.nombre).first()
        if existing_rol:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un rol con ese nombre"
            )
    
    # Actualizar campos
    for key, value in rol.dict(exclude_unset=True).items():
        setattr(db_rol, key, value)
    
    db_rol.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_rol)
    return db_rol

@router.delete("/{rol_id}", response_model=RolSchema)
def delete_rol(
    rol_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden eliminar roles"
        )
    
    db_rol = db.query(modelos.Rol).filter(modelos.Rol.id == rol_id).first()
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    
    # Verificar si hay usuarios asignados a este rol
    usuarios_count = db.query(func.count(modelos.Usuario.id)).filter(
        modelos.Usuario.rol_id == rol_id
    ).scalar()
    
    if usuarios_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar el rol porque tiene usuarios asignados"
        )
    
    db.delete(db_rol)
    db.commit()
    return db_rol

@router.get("/estadisticas/", response_model=RolEstadisticas)
def get_estadisticas_roles(
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden ver las estadísticas"
        )
    
    # Total de roles
    total_roles = db.query(func.count(modelos.Rol.id)).scalar()
    
    # Roles por estado
    roles_por_estado = dict(
        db.query(
            modelos.Estado.nombre,
            func.count(modelos.Rol.id)
        ).join(modelos.Rol).group_by(modelos.Estado.nombre).all()
    )
    
    # Roles por tipo de estado
    roles_por_tipo_estado = dict(
        db.query(
            modelos.TipoEstado.nombre,
            func.count(modelos.Rol.id)
        ).join(modelos.Rol).group_by(modelos.TipoEstado.nombre).all()
    )
    
    # Roles activos e inactivos
    roles_activos = db.query(func.count(modelos.Rol.id)).filter(
        modelos.Rol.estado_id == 1  # Asumiendo que 1 es el ID del estado "Activo"
    ).scalar()
    
    roles_inactivos = db.query(func.count(modelos.Rol.id)).filter(
        modelos.Rol.estado_id == 2  # Asumiendo que 2 es el ID del estado "Inactivo"
    ).scalar()
    
    # Roles por mes
    roles_por_mes = dict(
        db.query(
            func.date_trunc('month', modelos.Rol.fecha_creacion).label('mes'),
            func.count(modelos.Rol.id)
        ).group_by('mes').all()
    )
    
    # Promedio de usuarios por rol
    total_usuarios = db.query(func.count(modelos.Usuario.id)).scalar()
    promedio_usuarios = total_usuarios / total_roles if total_roles > 0 else 0
    
    # Roles por permiso
    roles = db.query(modelos.Rol).all()
    roles_por_permiso = {}
    for rol in roles:
        if rol.permisos:
            for permiso in rol.permisos:
                roles_por_permiso[permiso] = roles_por_permiso.get(permiso, 0) + 1
    
    return RolEstadisticas(
        total_roles=total_roles,
        roles_por_estado=roles_por_estado,
        roles_por_tipo_estado=roles_por_tipo_estado,
        roles_activos=roles_activos,
        roles_inactivos=roles_inactivos,
        roles_por_mes=roles_por_mes,
        promedio_usuarios=promedio_usuarios,
        roles_por_permiso=roles_por_permiso
    )
