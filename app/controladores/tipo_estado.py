from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional
from datetime import datetime

from app import modelos
from app.db.session import get_db
from app.esquemas.tipo_estado import (
    TipoEstado as TipoEstadoSchema,
    TipoEstadoCreate,
    TipoEstadoUpdate,
    TipoEstadoEstadisticas
)
from app.core.seguridad import get_current_user

router = APIRouter(
    prefix="/tipos-estado",
    tags=["tipos-estado"]
)

@router.get("/", response_model=List[TipoEstadoSchema])
def read_tipos_estado(
    skip: int = 0,
    limit: int = 100,
    activo: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden ver los tipos de estado"
        )
    
    query = db.query(modelos.TipoEstado)
    
    if activo is not None:
        query = query.filter(modelos.TipoEstado.activo == activo)
    if search:
        query = query.filter(
            or_(
                modelos.TipoEstado.nombre.ilike(f"%{search}%"),
                modelos.TipoEstado.descripcion.ilike(f"%{search}%"),
                modelos.TipoEstado.codigo.ilike(f"%{search}%")
            )
        )
    
    tipos_estado = query.order_by(modelos.TipoEstado.nombre).offset(skip).limit(limit).all()
    return tipos_estado

@router.get("/{tipo_estado_id}", response_model=TipoEstadoSchema)
def read_tipo_estado(
    tipo_estado_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden ver los tipos de estado"
        )
    
    tipo_estado = db.query(modelos.TipoEstado).filter(
        modelos.TipoEstado.id == tipo_estado_id
    ).first()
    if tipo_estado is None:
        raise HTTPException(status_code=404, detail="Tipo de estado no encontrado")
    return tipo_estado

@router.post("/", response_model=TipoEstadoSchema)
def create_tipo_estado(
    tipo_estado: TipoEstadoCreate,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden crear tipos de estado"
        )
    
    # Verificar que no existe un tipo con el mismo nombre o código
    tipo_existente = db.query(modelos.TipoEstado).filter(
        or_(
            modelos.TipoEstado.nombre == tipo_estado.nombre,
            modelos.TipoEstado.codigo == tipo_estado.codigo
        )
    ).first()
    
    if tipo_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un tipo de estado con ese nombre o código"
        )
    
    db_tipo_estado = modelos.TipoEstado(**tipo_estado.dict())
    db.add(db_tipo_estado)
    db.commit()
    db.refresh(db_tipo_estado)
    return db_tipo_estado

@router.put("/{tipo_estado_id}", response_model=TipoEstadoSchema)
def update_tipo_estado(
    tipo_estado_id: int,
    tipo_estado: TipoEstadoUpdate,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden actualizar tipos de estado"
        )
    
    db_tipo_estado = db.query(modelos.TipoEstado).filter(
        modelos.TipoEstado.id == tipo_estado_id
    ).first()
    if db_tipo_estado is None:
        raise HTTPException(status_code=404, detail="Tipo de estado no encontrado")
    
    # Si se está cambiando el nombre o código, verificar que no exista duplicado
    if tipo_estado.nombre or tipo_estado.codigo:
        nombre = tipo_estado.nombre or db_tipo_estado.nombre
        codigo = tipo_estado.codigo or db_tipo_estado.codigo
        
        tipo_existente = db.query(modelos.TipoEstado).filter(
            and_(
                or_(
                    modelos.TipoEstado.nombre == nombre,
                    modelos.TipoEstado.codigo == codigo
                ),
                modelos.TipoEstado.id != tipo_estado_id
            )
        ).first()
        
        if tipo_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un tipo de estado con ese nombre o código"
            )
    
    # Actualizar campos
    for key, value in tipo_estado.dict(exclude_unset=True).items():
        setattr(db_tipo_estado, key, value)
    
    db_tipo_estado.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_tipo_estado)
    return db_tipo_estado

@router.delete("/{tipo_estado_id}", response_model=TipoEstadoSchema)
def delete_tipo_estado(
    tipo_estado_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden eliminar tipos de estado"
        )
    
    db_tipo_estado = db.query(modelos.TipoEstado).filter(
        modelos.TipoEstado.id == tipo_estado_id
    ).first()
    if db_tipo_estado is None:
        raise HTTPException(status_code=404, detail="Tipo de estado no encontrado")
    
    # Verificar que no hay estados usando este tipo
    estados = db.query(func.count(modelos.Estado.id)).filter(
        modelos.Estado.tipo_estado_id == tipo_estado_id
    ).scalar()
    
    if estados > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar el tipo de estado porque hay estados que lo están usando"
        )
    
    db.delete(db_tipo_estado)
    db.commit()
    return db_tipo_estado

@router.get("/estadisticas/", response_model=TipoEstadoEstadisticas)
def get_estadisticas_tipos_estado(
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden ver las estadísticas"
        )
    
    # Total de tipos
    total_tipos = db.query(func.count(modelos.TipoEstado.id)).scalar()
    
    # Tipos activos/inactivos
    tipos_activos = db.query(func.count(modelos.TipoEstado.id)).filter(
        modelos.TipoEstado.activo == True
    ).scalar()
    
    tipos_inactivos = db.query(func.count(modelos.TipoEstado.id)).filter(
        modelos.TipoEstado.activo == False
    ).scalar()
    
    # Total de estados y distribución por tipo
    total_estados = db.query(func.count(modelos.Estado.id)).scalar()
    estados_por_tipo = dict(
        db.query(
            modelos.TipoEstado.nombre,
            func.count(modelos.Estado.id)
        ).join(modelos.Estado).group_by(modelos.TipoEstado.nombre).all()
    )
    
    # Total de entidades y distribución por tipo
    total_entidades = db.query(func.count(modelos.Proyecto.id)).scalar()
    entidades_por_tipo = dict(
        db.query(
            modelos.TipoEstado.nombre,
            func.count(modelos.Proyecto.id)
        ).join(modelos.Estado).join(modelos.Proyecto).group_by(modelos.TipoEstado.nombre).all()
    )
    
    return TipoEstadoEstadisticas(
        total_tipos=total_tipos,
        tipos_activos=tipos_activos,
        tipos_inactivos=tipos_inactivos,
        total_estados=total_estados,
        estados_por_tipo=estados_por_tipo,
        total_entidades=total_entidades,
        entidades_por_tipo=entidades_por_tipo
    )
