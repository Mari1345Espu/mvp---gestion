from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional
from datetime import datetime

from app import modelos
from app.db.session import get_db
from app.esquemas.convocatoria import (
    Convocatoria as ConvocatoriaSchema,
    ConvocatoriaCreate,
    ConvocatoriaUpdate,
    ConvocatoriaEstadisticas
)
from app.core.seguridad import get_current_user

router = APIRouter(
    prefix="/convocatorias",
    tags=["convocatorias"]
)

@router.get("/", response_model=List[ConvocatoriaSchema])
def read_convocatorias(
    skip: int = 0,
    limit: int = 100,
    estado_id: Optional[int] = None,
    tipo_proyecto_id: Optional[int] = None,
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    query = db.query(modelos.Convocatoria)
    
    if estado_id:
        query = query.filter(modelos.Convocatoria.estado_id == estado_id)
    if tipo_proyecto_id:
        query = query.filter(modelos.Convocatoria.tipo_proyecto_id == tipo_proyecto_id)
    if fecha_inicio and fecha_fin:
        query = query.filter(
            and_(
                modelos.Convocatoria.fecha_inicio >= fecha_inicio,
                modelos.Convocatoria.fecha_fin <= fecha_fin
            )
        )
    if search:
        query = query.filter(
            or_(
                modelos.Convocatoria.nombre.ilike(f"%{search}%"),
                modelos.Convocatoria.descripcion.ilike(f"%{search}%")
            )
        )
    
    convocatorias = query.offset(skip).limit(limit).all()
    return convocatorias

@router.get("/{convocatoria_id}", response_model=ConvocatoriaSchema)
def read_convocatoria(
    convocatoria_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    convocatoria = db.query(modelos.Convocatoria).filter(
        modelos.Convocatoria.id == convocatoria_id
    ).first()
    if convocatoria is None:
        raise HTTPException(status_code=404, detail="Convocatoria no encontrada")
    return convocatoria

@router.post("/", response_model=ConvocatoriaSchema)
def create_convocatoria(
    convocatoria: ConvocatoriaCreate,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden crear convocatorias"
        )
    
    # Verificar que el nombre no esté duplicado
    existing_convocatoria = db.query(modelos.Convocatoria).filter(
        modelos.Convocatoria.nombre == convocatoria.nombre
    ).first()
    if existing_convocatoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una convocatoria con ese nombre"
        )
    
    # Verificar que la fecha de inicio sea anterior a la fecha de fin
    if convocatoria.fecha_inicio >= convocatoria.fecha_fin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de inicio debe ser anterior a la fecha de fin"
        )
    
    db_convocatoria = modelos.Convocatoria(**convocatoria.dict())
    db.add(db_convocatoria)
    db.commit()
    db.refresh(db_convocatoria)
    return db_convocatoria

@router.put("/{convocatoria_id}", response_model=ConvocatoriaSchema)
def update_convocatoria(
    convocatoria_id: int,
    convocatoria: ConvocatoriaUpdate,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden actualizar convocatorias"
        )
    
    db_convocatoria = db.query(modelos.Convocatoria).filter(
        modelos.Convocatoria.id == convocatoria_id
    ).first()
    if db_convocatoria is None:
        raise HTTPException(status_code=404, detail="Convocatoria no encontrada")
    
    # Verificar que el nuevo nombre no esté duplicado si se está actualizando
    if convocatoria.nombre and convocatoria.nombre != db_convocatoria.nombre:
        existing_convocatoria = db.query(modelos.Convocatoria).filter(
            modelos.Convocatoria.nombre == convocatoria.nombre
        ).first()
        if existing_convocatoria:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe una convocatoria con ese nombre"
            )
    
    # Verificar fechas si se están actualizando
    if convocatoria.fecha_inicio and convocatoria.fecha_fin:
        if convocatoria.fecha_inicio >= convocatoria.fecha_fin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La fecha de inicio debe ser anterior a la fecha de fin"
            )
    
    # Actualizar campos
    for key, value in convocatoria.dict(exclude_unset=True).items():
        setattr(db_convocatoria, key, value)
    
    db_convocatoria.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_convocatoria)
    return db_convocatoria

@router.delete("/{convocatoria_id}", response_model=ConvocatoriaSchema)
def delete_convocatoria(
    convocatoria_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden eliminar convocatorias"
        )
    
    db_convocatoria = db.query(modelos.Convocatoria).filter(
        modelos.Convocatoria.id == convocatoria_id
    ).first()
    if db_convocatoria is None:
        raise HTTPException(status_code=404, detail="Convocatoria no encontrada")
    
    # Verificar si hay proyectos asociados
    proyectos_count = db.query(func.count(modelos.Proyecto.id)).filter(
        modelos.Proyecto.convocatoria_id == convocatoria_id
    ).scalar()
    
    if proyectos_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar la convocatoria porque tiene proyectos asociados"
        )
    
    db.delete(db_convocatoria)
    db.commit()
    return db_convocatoria

@router.get("/estadisticas/", response_model=ConvocatoriaEstadisticas)
def get_estadisticas_convocatorias(
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden ver las estadísticas"
        )
    
    # Total de convocatorias
    total_convocatorias = db.query(func.count(modelos.Convocatoria.id)).scalar()
    
    # Convocatorias por estado
    convocatorias_por_estado = dict(
        db.query(
            modelos.Estado.nombre,
            func.count(modelos.Convocatoria.id)
        ).join(modelos.Convocatoria).group_by(modelos.Estado.nombre).all()
    )
    
    # Convocatorias por tipo de estado
    convocatorias_por_tipo_estado = dict(
        db.query(
            modelos.TipoEstado.nombre,
            func.count(modelos.Convocatoria.id)
        ).join(modelos.Convocatoria).group_by(modelos.TipoEstado.nombre).all()
    )
    
    # Convocatorias por tipo de proyecto
    convocatorias_por_tipo_proyecto = dict(
        db.query(
            modelos.TipoProyecto.nombre,
            func.count(modelos.Convocatoria.id)
        ).join(modelos.Convocatoria).group_by(modelos.TipoProyecto.nombre).all()
    )
    
    # Convocatorias activas y finalizadas
    convocatorias_activas = db.query(func.count(modelos.Convocatoria.id)).filter(
        and_(
            modelos.Convocatoria.fecha_inicio <= datetime.utcnow(),
            modelos.Convocatoria.fecha_fin >= datetime.utcnow()
        )
    ).scalar()
    
    convocatorias_finalizadas = db.query(func.count(modelos.Convocatoria.id)).filter(
        modelos.Convocatoria.fecha_fin < datetime.utcnow()
    ).scalar()
    
    # Convocatorias por mes
    convocatorias_por_mes = dict(
        db.query(
            func.date_trunc('month', modelos.Convocatoria.fecha_creacion).label('mes'),
            func.count(modelos.Convocatoria.id)
        ).group_by('mes').all()
    )
    
    # Promedios y totales
    convocatorias = db.query(modelos.Convocatoria).all()
    total_proyectos = 0
    total_presupuesto = 0
    proyectos_por_convocatoria = {}
    
    for convocatoria in convocatorias:
        # Contar proyectos
        proyectos = db.query(func.count(modelos.Proyecto.id)).filter(
            modelos.Proyecto.convocatoria_id == convocatoria.id
        ).scalar()
        total_proyectos += proyectos
        proyectos_por_convocatoria[convocatoria.nombre] = proyectos
        
        # Sumar presupuesto
        presupuesto = db.query(func.sum(modelos.Proyecto.presupuesto)).filter(
            modelos.Proyecto.convocatoria_id == convocatoria.id
        ).scalar() or 0
        total_presupuesto += presupuesto
    
    promedio_proyectos = total_proyectos / total_convocatorias if total_convocatorias > 0 else 0
    promedio_presupuesto = total_presupuesto / total_convocatorias if total_convocatorias > 0 else 0
    
    return ConvocatoriaEstadisticas(
        total_convocatorias=total_convocatorias,
        convocatorias_por_estado=convocatorias_por_estado,
        convocatorias_por_tipo_estado=convocatorias_por_tipo_estado,
        convocatorias_por_tipo_proyecto=convocatorias_por_tipo_proyecto,
        convocatorias_activas=convocatorias_activas,
        convocatorias_finalizadas=convocatorias_finalizadas,
        convocatorias_por_mes=convocatorias_por_mes,
        promedio_proyectos=promedio_proyectos,
        promedio_presupuesto=promedio_presupuesto,
        total_presupuesto_asignado=total_presupuesto,
        proyectos_por_convocatoria=proyectos_por_convocatoria
    )
