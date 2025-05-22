from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional
from datetime import datetime

from app import modelos
from app.db.session import get_db
from app.esquemas.estado import (
    Estado as EstadoSchema,
    EstadoCreate,
    EstadoUpdate,
    EstadoEstadisticas
)
from app.core.seguridad import get_current_user

router = APIRouter(
    prefix="/estados",
    tags=["estados"]
)

@router.get("/", response_model=List[EstadoSchema])
def read_estados(
    skip: int = 0,
    limit: int = 100,
    tipo_estado_id: Optional[int] = None,
    activo: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden ver los estados"
        )
    
    query = db.query(modelos.Estado)
    
    if tipo_estado_id:
        query = query.filter(modelos.Estado.tipo_estado_id == tipo_estado_id)
    if activo is not None:
        query = query.filter(modelos.Estado.activo == activo)
    if search:
        query = query.filter(
            or_(
                modelos.Estado.nombre.ilike(f"%{search}%"),
                modelos.Estado.descripcion.ilike(f"%{search}%")
            )
        )
    
    estados = query.order_by(modelos.Estado.orden).offset(skip).limit(limit).all()
    return estados

@router.get("/{estado_id}", response_model=EstadoSchema)
def read_estado(
    estado_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden ver los estados"
        )
    
    estado = db.query(modelos.Estado).filter(
        modelos.Estado.id == estado_id
    ).first()
    if estado is None:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    return estado

@router.post("/", response_model=EstadoSchema)
def create_estado(
    estado: EstadoCreate,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden crear estados"
        )
    
    # Verificar que el tipo de estado existe
    tipo_estado = db.query(modelos.TipoEstado).filter(
        modelos.TipoEstado.id == estado.tipo_estado_id
    ).first()
    if not tipo_estado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El tipo de estado especificado no existe"
        )
    
    # Verificar que no existe un estado con el mismo nombre para el mismo tipo
    estado_existente = db.query(modelos.Estado).filter(
        and_(
            modelos.Estado.nombre == estado.nombre,
            modelos.Estado.tipo_estado_id == estado.tipo_estado_id
        )
    ).first()
    
    if estado_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un estado con ese nombre para este tipo"
        )
    
    db_estado = modelos.Estado(**estado.dict())
    db.add(db_estado)
    db.commit()
    db.refresh(db_estado)
    return db_estado

@router.put("/{estado_id}", response_model=EstadoSchema)
def update_estado(
    estado_id: int,
    estado: EstadoUpdate,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden actualizar estados"
        )
    
    db_estado = db.query(modelos.Estado).filter(
        modelos.Estado.id == estado_id
    ).first()
    if db_estado is None:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    
    # Si se está cambiando el nombre o el tipo, verificar que no exista duplicado
    if estado.nombre or estado.tipo_estado_id:
        nombre = estado.nombre or db_estado.nombre
        tipo_id = estado.tipo_estado_id or db_estado.tipo_estado_id
        
        estado_existente = db.query(modelos.Estado).filter(
            and_(
                modelos.Estado.nombre == nombre,
                modelos.Estado.tipo_estado_id == tipo_id,
                modelos.Estado.id != estado_id
            )
        ).first()
        
        if estado_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un estado con ese nombre para este tipo"
            )
    
    # Actualizar campos
    for key, value in estado.dict(exclude_unset=True).items():
        setattr(db_estado, key, value)
    
    db_estado.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_estado)
    return db_estado

@router.delete("/{estado_id}", response_model=EstadoSchema)
def delete_estado(
    estado_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden eliminar estados"
        )
    
    db_estado = db.query(modelos.Estado).filter(
        modelos.Estado.id == estado_id
    ).first()
    if db_estado is None:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    
    # Verificar que no hay entidades usando este estado
    entidades = db.query(func.count(modelos.Proyecto.id)).filter(
        modelos.Proyecto.estado_id == estado_id
    ).scalar()
    
    if entidades > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar el estado porque hay entidades que lo están usando"
        )
    
    db.delete(db_estado)
    db.commit()
    return db_estado

@router.get("/estadisticas/", response_model=EstadoEstadisticas)
def get_estadisticas_estados(
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden ver las estadísticas"
        )
    
    # Total de estados
    total_estados = db.query(func.count(modelos.Estado.id)).scalar()
    
    # Estados por tipo
    estados_por_tipo = dict(
        db.query(
            modelos.TipoEstado.nombre,
            func.count(modelos.Estado.id)
        ).join(modelos.Estado).group_by(modelos.TipoEstado.nombre).all()
    )
    
    # Estados activos/inactivos
    estados_activos = db.query(func.count(modelos.Estado.id)).filter(
        modelos.Estado.activo == True
    ).scalar()
    
    estados_inactivos = db.query(func.count(modelos.Estado.id)).filter(
        modelos.Estado.activo == False
    ).scalar()
    
    # Estados por orden
    estados_por_orden = dict(
        db.query(
            modelos.Estado.orden,
            func.count(modelos.Estado.id)
        ).group_by(modelos.Estado.orden).all()
    )
    
    # Total de entidades y distribución por estado
    total_entidades = db.query(func.count(modelos.Proyecto.id)).scalar()
    entidades_por_estado = dict(
        db.query(
            modelos.Estado.nombre,
            func.count(modelos.Proyecto.id)
        ).join(modelos.Proyecto).group_by(modelos.Estado.nombre).all()
    )
    
    return EstadoEstadisticas(
        total_estados=total_estados,
        estados_por_tipo=estados_por_tipo,
        estados_activos=estados_activos,
        estados_inactivos=estados_inactivos,
        estados_por_orden=estados_por_orden,
        total_entidades=total_entidades,
        entidades_por_estado=entidades_por_estado
    )
