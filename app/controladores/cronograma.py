from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, extract
from typing import List, Optional
from datetime import datetime, timedelta

from app import modelos
from app.db.session import get_db
from app.esquemas.cronograma import (
    Cronograma as CronogramaSchema,
    CronogramaCreate,
    CronogramaUpdate,
    CronogramaEstadisticas
)
from app.core.seguridad import get_current_user

router = APIRouter(
    prefix="/cronogramas",
    tags=["cronogramas"]
)

@router.get("/", response_model=List[CronogramaSchema])
def read_cronogramas(
    skip: int = 0,
    limit: int = 100,
    proyecto_id: Optional[int] = None,
    responsable_id: Optional[int] = None,
    estado_id: Optional[int] = None,
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    query = db.query(modelos.Cronograma)
    
    if proyecto_id:
        query = query.filter(modelos.Cronograma.proyecto_id == proyecto_id)
    if responsable_id:
        query = query.filter(modelos.Cronograma.responsable_id == responsable_id)
    if estado_id:
        query = query.filter(modelos.Cronograma.estado_id == estado_id)
    if fecha_inicio and fecha_fin:
        query = query.filter(
            and_(
                modelos.Cronograma.fecha_inicio >= fecha_inicio,
                modelos.Cronograma.fecha_fin <= fecha_fin
            )
        )
    if search:
        query = query.filter(
            or_(
                modelos.Cronograma.nombre.ilike(f"%{search}%"),
                modelos.Cronograma.descripcion.ilike(f"%{search}%")
            )
        )
    
    cronogramas = query.offset(skip).limit(limit).all()
    return cronogramas

@router.get("/{cronograma_id}", response_model=CronogramaSchema)
def read_cronograma(
    cronograma_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    cronograma = db.query(modelos.Cronograma).filter(
        modelos.Cronograma.id == cronograma_id
    ).first()
    if cronograma is None:
        raise HTTPException(status_code=404, detail="Cronograma no encontrado")
    return cronograma

@router.post("/", response_model=CronogramaSchema)
def create_cronograma(
    cronograma: CronogramaCreate,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre not in ["Admin", "Investigador"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para crear cronogramas"
        )
    
    # Verificar que el proyecto existe
    proyecto = db.query(modelos.Proyecto).filter(
        modelos.Proyecto.id == cronograma.proyecto_id
    ).first()
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El proyecto especificado no existe"
        )
    
    # Verificar que las fechas son válidas
    if cronograma.fecha_inicio >= cronograma.fecha_fin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de inicio debe ser anterior a la fecha de fin"
        )
    
    # Verificar que las fechas están dentro del rango del proyecto
    if cronograma.fecha_inicio < proyecto.fecha_inicio or cronograma.fecha_fin > proyecto.fecha_fin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Las fechas del cronograma deben estar dentro del rango del proyecto"
        )
    
    # Verificar dependencias si existen
    if cronograma.dependencias:
        for dep_id in cronograma.dependencias:
            dep = db.query(modelos.Cronograma).filter(
                modelos.Cronograma.id == dep_id
            ).first()
            if not dep:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"La dependencia con ID {dep_id} no existe"
                )
            if dep.fecha_fin > cronograma.fecha_inicio:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"La dependencia {dep_id} termina después del inicio de este cronograma"
                )
    
    db_cronograma = modelos.Cronograma(**cronograma.dict())
    db.add(db_cronograma)
    db.commit()
    db.refresh(db_cronograma)
    return db_cronograma

@router.put("/{cronograma_id}", response_model=CronogramaSchema)
def update_cronograma(
    cronograma_id: int,
    cronograma: CronogramaUpdate,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre not in ["Admin", "Investigador"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para actualizar cronogramas"
        )
    
    db_cronograma = db.query(modelos.Cronograma).filter(
        modelos.Cronograma.id == cronograma_id
    ).first()
    if db_cronograma is None:
        raise HTTPException(status_code=404, detail="Cronograma no encontrado")
    
    # Verificar permisos específicos
    if current_user.rol.nombre != "Admin" and db_cronograma.responsable_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo puede actualizar sus propios cronogramas"
        )
    
    # Verificar fechas si se están actualizando
    if cronograma.fecha_inicio and cronograma.fecha_fin:
        if cronograma.fecha_inicio >= cronograma.fecha_fin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La fecha de inicio debe ser anterior a la fecha de fin"
            )
        
        # Verificar que las fechas están dentro del rango del proyecto
        proyecto = db.query(modelos.Proyecto).filter(
            modelos.Proyecto.id == db_cronograma.proyecto_id
        ).first()
        if cronograma.fecha_inicio < proyecto.fecha_inicio or cronograma.fecha_fin > proyecto.fecha_fin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Las fechas del cronograma deben estar dentro del rango del proyecto"
            )
    
    # Verificar dependencias si se están actualizando
    if cronograma.dependencias:
        for dep_id in cronograma.dependencias:
            if dep_id == cronograma_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Un cronograma no puede depender de sí mismo"
                )
            dep = db.query(modelos.Cronograma).filter(
                modelos.Cronograma.id == dep_id
            ).first()
            if not dep:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"La dependencia con ID {dep_id} no existe"
                )
            if dep.fecha_fin > (cronograma.fecha_inicio or db_cronograma.fecha_inicio):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"La dependencia {dep_id} termina después del inicio de este cronograma"
                )
    
    # Actualizar campos
    for key, value in cronograma.dict(exclude_unset=True).items():
        setattr(db_cronograma, key, value)
    
    db_cronograma.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_cronograma)
    return db_cronograma

@router.delete("/{cronograma_id}", response_model=CronogramaSchema)
def delete_cronograma(
    cronograma_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden eliminar cronogramas"
        )
    
    db_cronograma = db.query(modelos.Cronograma).filter(
        modelos.Cronograma.id == cronograma_id
    ).first()
    if db_cronograma is None:
        raise HTTPException(status_code=404, detail="Cronograma no encontrado")
    
    # Verificar si hay otros cronogramas que dependen de este
    dependientes = db.query(modelos.Cronograma).filter(
        modelos.Cronograma.dependencias.contains([cronograma_id])
    ).first()
    if dependientes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar el cronograma porque hay otros que dependen de él"
        )
    
    db.delete(db_cronograma)
    db.commit()
    return db_cronograma

@router.get("/estadisticas/", response_model=CronogramaEstadisticas)
def get_estadisticas_cronogramas(
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden ver las estadísticas"
        )
    
    # Total de cronogramas
    total_cronogramas = db.query(func.count(modelos.Cronograma.id)).scalar()
    
    # Cronogramas por estado
    cronogramas_por_estado = dict(
        db.query(
            modelos.Estado.nombre,
            func.count(modelos.Cronograma.id)
        ).join(modelos.Cronograma).group_by(modelos.Estado.nombre).all()
    )
    
    # Cronogramas por tipo de estado
    cronogramas_por_tipo_estado = dict(
        db.query(
            modelos.TipoEstado.nombre,
            func.count(modelos.Cronograma.id)
        ).join(modelos.Cronograma).group_by(modelos.TipoEstado.nombre).all()
    )
    
    # Cronogramas por proyecto
    cronogramas_por_proyecto = dict(
        db.query(
            modelos.Proyecto.nombre,
            func.count(modelos.Cronograma.id)
        ).join(modelos.Cronograma).group_by(modelos.Proyecto.nombre).all()
    )
    
    # Cronogramas por responsable
    cronogramas_por_responsable = dict(
        db.query(
            modelos.Usuario.nombre,
            func.count(modelos.Cronograma.id)
        ).join(modelos.Cronograma).group_by(modelos.Usuario.nombre).all()
    )
    
    # Cronogramas por mes
    cronogramas_por_mes = dict(
        db.query(
            func.date_trunc('month', modelos.Cronograma.fecha_creacion).label('mes'),
            func.count(modelos.Cronograma.id)
        ).group_by('mes').all()
    )
    
    # Cronogramas atrasados, completados y en progreso
    ahora = datetime.utcnow()
    cronogramas_atrasados = db.query(func.count(modelos.Cronograma.id)).filter(
        and_(
            modelos.Cronograma.fecha_fin < ahora,
            modelos.Cronograma.porcentaje_avance < 100
        )
    ).scalar()
    
    cronogramas_completados = db.query(func.count(modelos.Cronograma.id)).filter(
        modelos.Cronograma.porcentaje_avance == 100
    ).scalar()
    
    cronogramas_en_progreso = db.query(func.count(modelos.Cronograma.id)).filter(
        and_(
            modelos.Cronograma.porcentaje_avance > 0,
            modelos.Cronograma.porcentaje_avance < 100
        )
    ).scalar()
    
    # Promedios
    cronogramas = db.query(modelos.Cronograma).all()
    promedio_avance = sum(c.porcentaje_avance or 0 for c in cronogramas) / total_cronogramas if total_cronogramas > 0 else 0
    
    duraciones = [(c.fecha_fin - c.fecha_inicio).days for c in cronogramas]
    promedio_duracion = sum(duraciones) / len(duraciones) if duraciones else 0
    
    atrasos = [(ahora - c.fecha_fin).days for c in cronogramas if c.fecha_fin < ahora]
    promedio_atraso = sum(atrasos) / len(atrasos) if atrasos else 0
    
    # Costos
    total_costo_estimado = sum(c.costo_estimado or 0 for c in cronogramas)
    total_costo_real = sum(c.costo_real or 0 for c in cronogramas)
    variacion_costo = total_costo_real - total_costo_estimado
    
    return CronogramaEstadisticas(
        total_cronogramas=total_cronogramas,
        cronogramas_por_estado=cronogramas_por_estado,
        cronogramas_por_tipo_estado=cronogramas_por_tipo_estado,
        cronogramas_por_proyecto=cronogramas_por_proyecto,
        cronogramas_por_responsable=cronogramas_por_responsable,
        cronogramas_por_mes=cronogramas_por_mes,
        cronogramas_atrasados=cronogramas_atrasados,
        cronogramas_completados=cronogramas_completados,
        cronogramas_en_progreso=cronogramas_en_progreso,
        promedio_avance=promedio_avance,
        promedio_duracion=promedio_duracion,
        promedio_atraso=promedio_atraso,
        total_costo_estimado=total_costo_estimado,
        total_costo_real=total_costo_real,
        variacion_costo=variacion_costo
    )
