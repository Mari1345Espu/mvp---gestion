from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.modelos import avance as models
from app.modelos.usuario import Usuario
from app.esquemas import avance as schemas
from app.dependencias import auth
from datetime import datetime
from sqlalchemy import and_, func

router = APIRouter(
    prefix="/avances",
    tags=["avances"]
)

@router.post("/", response_model=schemas.Avance)
def create_avance(
    avance: schemas.AvanceCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth.get_current_user)
):
    """Crea un nuevo avance."""
    db_avance = models.Avance(**avance.dict())
    db.add(db_avance)
    db.commit()
    db.refresh(db_avance)
    return db_avance

@router.get("/", response_model=List[schemas.Avance])
def read_avances(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth.get_current_user)
):
    """Obtiene todos los avances."""
    avances = db.query(models.Avance).offset(skip).limit(limit).all()
    return avances

@router.get("/{avance_id}", response_model=schemas.Avance)
def read_avance(
    avance_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth.get_current_user)
):
    """Obtiene un avance específico por su ID."""
    db_avance = db.query(models.Avance).filter(models.Avance.id == avance_id).first()
    if db_avance is None:
        raise HTTPException(status_code=404, detail="Avance no encontrado")
    return db_avance

@router.put("/{avance_id}", response_model=schemas.Avance)
def update_avance(
    avance_id: int,
    avance: schemas.AvanceUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth.get_current_user)
):
    """Actualiza un avance existente."""
    db_avance = db.query(models.Avance).filter(models.Avance.id == avance_id).first()
    if db_avance is None:
        raise HTTPException(status_code=404, detail="Avance no encontrado")
    
    for key, value in avance.dict(exclude_unset=True).items():
        setattr(db_avance, key, value)
    
    db.commit()
    db.refresh(db_avance)
    return db_avance

@router.delete("/{avance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_avance(
    avance_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth.get_current_user)
):
    """Elimina un avance."""
    db_avance = db.query(models.Avance).filter(models.Avance.id == avance_id).first()
    if db_avance is None:
        raise HTTPException(status_code=404, detail="Avance no encontrado")
    
    db.delete(db_avance)
    db.commit()
    return None

@router.get("/proyecto/{proyecto_id}", response_model=List[schemas.Avance])
def read_avances_by_proyecto(
    proyecto_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth.get_current_user)
):
    avances = db.query(models.Avance).filter(
        models.Avance.proyecto_id == proyecto_id
    ).all()
    return avances

@router.get("/tarea/{tarea_id}", response_model=List[schemas.Avance])
def read_avances_by_tarea(
    tarea_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth.get_current_user)
):
    avances = db.query(models.Avance).filter(
        models.Avance.tarea_id == tarea_id
    ).all()
    return avances

@router.put("/{avance_id}/aprobar", response_model=schemas.Avance)
def aprobar_avance(
    avance_id: int,
    observaciones: str = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth.get_current_user)
):
    db_avance = db.query(models.Avance).filter(models.Avance.id == avance_id).first()
    if db_avance is None:
        raise HTTPException(status_code=404, detail="Avance no encontrado")
    
    db_avance.aprobado = True
    db_avance.fecha_aprobacion = datetime.utcnow()
    db_avance.aprobado_por_id = current_user.id
    if observaciones:
        db_avance.observaciones = observaciones
    
    db.commit()
    db.refresh(db_avance)
    return db_avance

@router.get("/estado/{estado_id}", response_model=List[schemas.Avance])
def read_avances_by_estado(
    estado_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth.get_current_user)
):
    avances = db.query(models.Avance).filter(
        models.Avance.estado_id == estado_id
    ).all()
    return avances

@router.get("/fecha/{fecha_inicio}/{fecha_fin}", response_model=List[schemas.Avance])
def read_avances_by_fecha(
    fecha_inicio: datetime,
    fecha_fin: datetime,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth.get_current_user)
):
    avances = db.query(models.Avance).filter(
        and_(
            models.Avance.fecha_creacion >= fecha_inicio,
            models.Avance.fecha_creacion <= fecha_fin
        )
    ).all()
    return avances

@router.get("/estadisticas/", response_model=dict)
def get_estadisticas_avances(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth.get_current_user)
):
    total_avances = db.query(models.Avance).count()
    avances_aprobados = db.query(models.Avance).filter(
        models.Avance.aprobado == True
    ).count()
    promedio_completado = db.query(func.avg(models.Avance.porcentaje_completado)).scalar() or 0
    
    return {
        "total_avances": total_avances,
        "avances_aprobados": avances_aprobados,
        "avances_pendientes": total_avances - avances_aprobados,
        "promedio_completado": round(promedio_completado, 2)
    }

@router.put("/{avance_id}/completado", response_model=schemas.Avance)
def actualizar_porcentaje_completado(
    avance_id: int,
    porcentaje_completado: float,
    observaciones: str = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth.get_current_user)
):
    db_avance = db.query(models.Avance).filter(models.Avance.id == avance_id).first()
    if db_avance is None:
        raise HTTPException(status_code=404, detail="Avance no encontrado")
    
    if porcentaje_completado < 0 or porcentaje_completado > 100:
        raise HTTPException(status_code=400, detail="El porcentaje de completado debe estar entre 0 y 100")
    
    db_avance.porcentaje_completado = porcentaje_completado
    if observaciones:
        db_avance.observaciones = observaciones
    
    db.commit()
    db.refresh(db_avance)
    return db_avance
