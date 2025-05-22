from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.modelos import tarea as models
from app.modelos.usuario import Usuario
from app.esquemas import tarea as schemas
from app.dependencias import auth
from datetime import datetime
from sqlalchemy import and_, func

router = APIRouter(
    prefix="/tareas",
    tags=["tareas"]
)

@router.post("/", response_model=schemas.Tarea)
def create_tarea(
    tarea: schemas.TareaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth.get_current_user)
):
    """Crea una nueva tarea."""
    db_tarea = models.Tarea(**tarea.dict())
    db.add(db_tarea)
    db.commit()
    db.refresh(db_tarea)
    return db_tarea

@router.get("/", response_model=List[schemas.Tarea])
def read_tareas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth.get_current_user)
):
    """Obtiene todas las tareas."""
    tareas = db.query(models.Tarea).offset(skip).limit(limit).all()
    return tareas

@router.get("/{tarea_id}", response_model=schemas.Tarea)
def read_tarea(
    tarea_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth.get_current_user)
):
    """Obtiene una tarea específica por su ID."""
    db_tarea = db.query(models.Tarea).filter(models.Tarea.id == tarea_id).first()
    if db_tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_tarea

@router.put("/{tarea_id}", response_model=schemas.Tarea)
def update_tarea(
    tarea_id: int,
    tarea: schemas.TareaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth.get_current_user)
):
    """Actualiza una tarea existente."""
    db_tarea = db.query(models.Tarea).filter(models.Tarea.id == tarea_id).first()
    if db_tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    for key, value in tarea.dict(exclude_unset=True).items():
        setattr(db_tarea, key, value)
    
    db.commit()
    db.refresh(db_tarea)
    return db_tarea

@router.delete("/{tarea_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tarea(
    tarea_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth.get_current_user)
):
    """Elimina una tarea."""
    db_tarea = db.query(models.Tarea).filter(models.Tarea.id == tarea_id).first()
    if db_tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    db.delete(db_tarea)
    db.commit()
    return None

@router.get("/proyecto/{proyecto_id}", response_model=List[schemas.Tarea])
def read_tareas_by_proyecto(
    proyecto_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth.get_current_user)
):
    """Obtiene todas las tareas de un proyecto específico."""
    tareas = db.query(models.Tarea).filter(
        models.Tarea.proyecto_id == proyecto_id
    ).all()
    return tareas

@router.get("/estado/{estado_id}", response_model=List[schemas.Tarea])
def read_tareas_by_estado(
    estado_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth.get_current_user)
):
    """Obtiene todas las tareas con un estado específico."""
    tareas = db.query(models.Tarea).filter(
        models.Tarea.estado_id == estado_id
    ).all()
    return tareas

@router.get("/responsable/{responsable_id}", response_model=List[schemas.Tarea])
def read_tareas_by_responsable(
    responsable_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth.get_current_user)
):
    """Obtiene todas las tareas asignadas a un responsable específico."""
    tareas = db.query(models.Tarea).filter(
        models.Tarea.responsable_id == responsable_id
    ).all()
    return tareas

@router.get("/fecha/{fecha_inicio}/{fecha_fin}", response_model=List[schemas.Tarea])
def read_tareas_by_fecha(
    fecha_inicio: datetime,
    fecha_fin: datetime,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth.get_current_user)
):
    """Obtiene todas las tareas creadas entre dos fechas."""
    tareas = db.query(models.Tarea).filter(
        and_(
            models.Tarea.fecha_creacion >= fecha_inicio,
            models.Tarea.fecha_creacion <= fecha_fin
        )
    ).all()
    return tareas

@router.get("/estadisticas/", response_model=dict)
def get_estadisticas_tareas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth.get_current_user)
):
    """Obtiene estadísticas generales de las tareas."""
    total_tareas = db.query(models.Tarea).count()
    tareas_completadas = db.query(models.Tarea).filter(
        models.Tarea.estado_id == 3  # Asumiendo que 3 es el ID del estado "Completado"
    ).count()
    promedio_duracion = db.query(func.avg(
        func.extract('epoch', models.Tarea.fecha_fin - models.Tarea.fecha_inicio)
    )).scalar() or 0
    
    return {
        "total_tareas": total_tareas,
        "tareas_completadas": tareas_completadas,
        "tareas_pendientes": total_tareas - tareas_completadas,
        "promedio_duracion_dias": round(promedio_duracion / 86400, 2)  # Convertir segundos a días
    }

@router.put("/{tarea_id}/avance", response_model=schemas.Tarea)
def actualizar_avance_tarea(
    tarea_id: int,
    porcentaje_avance: float,
    observaciones: str = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(auth.get_current_user)
):
    db_tarea = db.query(models.Tarea).filter(models.Tarea.id == tarea_id).first()
    if db_tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    if porcentaje_avance < 0 or porcentaje_avance > 100:
        raise HTTPException(status_code=400, detail="El porcentaje de avance debe estar entre 0 y 100")
    
    db_tarea.porcentaje_avance = porcentaje_avance
    db_tarea.fecha_ultimo_avance = datetime.utcnow()
    if observaciones:
        db_tarea.observaciones = observaciones
    
    db.commit()
    db.refresh(db_tarea)
    return db_tarea
