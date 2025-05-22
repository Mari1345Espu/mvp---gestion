from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.modelos import conceptoevaluacion as models
from app.esquemas import conceptoevaluacion as schemas
from app.controladores import auth
from datetime import datetime
from sqlalchemy import and_
from sqlalchemy.sql import func

router = APIRouter(
    prefix="/conceptos-evaluacion",
    tags=["conceptos-evaluacion"]
)

@router.post("/", response_model=schemas.ConceptoEvaluacion)
def create_concepto_evaluacion(
    concepto: schemas.ConceptoEvaluacionCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    db_concepto = models.ConceptoEvaluacion(**concepto.dict())
    db.add(db_concepto)
    db.commit()
    db.refresh(db_concepto)
    return db_concepto

@router.get("/", response_model=List[schemas.ConceptoEvaluacion])
def read_conceptos_evaluacion(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    conceptos = db.query(models.ConceptoEvaluacion).offset(skip).limit(limit).all()
    return conceptos

@router.get("/{concepto_id}", response_model=schemas.ConceptoEvaluacion)
def read_concepto_evaluacion(
    concepto_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    db_concepto = db.query(models.ConceptoEvaluacion).filter(models.ConceptoEvaluacion.id == concepto_id).first()
    if db_concepto is None:
        raise HTTPException(status_code=404, detail="Concepto de evaluación no encontrado")
    return db_concepto

@router.put("/{concepto_id}", response_model=schemas.ConceptoEvaluacion)
def update_concepto_evaluacion(
    concepto_id: int,
    concepto: schemas.ConceptoEvaluacionUpdate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    db_concepto = db.query(models.ConceptoEvaluacion).filter(models.ConceptoEvaluacion.id == concepto_id).first()
    if db_concepto is None:
        raise HTTPException(status_code=404, detail="Concepto de evaluación no encontrado")
    
    for key, value in concepto.dict(exclude_unset=True).items():
        setattr(db_concepto, key, value)
    
    db.commit()
    db.refresh(db_concepto)
    return db_concepto

@router.delete("/{concepto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_concepto_evaluacion(
    concepto_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    db_concepto = db.query(models.ConceptoEvaluacion).filter(models.ConceptoEvaluacion.id == concepto_id).first()
    if db_concepto is None:
        raise HTTPException(status_code=404, detail="Concepto de evaluación no encontrado")
    
    db.delete(db_concepto)
    db.commit()
    return None

@router.get("/proyecto/{proyecto_id}", response_model=List[schemas.ConceptoEvaluacion])
def read_conceptos_evaluacion_by_proyecto(
    proyecto_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    conceptos = db.query(models.ConceptoEvaluacion).filter(
        models.ConceptoEvaluacion.proyecto_id == proyecto_id
    ).all()
    return conceptos

@router.get("/evaluador/{evaluador_id}", response_model=List[schemas.ConceptoEvaluacion])
def read_conceptos_evaluacion_by_evaluador(
    evaluador_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    conceptos = db.query(models.ConceptoEvaluacion).filter(
        models.ConceptoEvaluacion.evaluador_id == evaluador_id
    ).all()
    return conceptos

@router.put("/{concepto_id}/aprobar", response_model=schemas.ConceptoEvaluacion)
def aprobar_concepto_evaluacion(
    concepto_id: int,
    observaciones: str = None,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    db_concepto = db.query(models.ConceptoEvaluacion).filter(models.ConceptoEvaluacion.id == concepto_id).first()
    if db_concepto is None:
        raise HTTPException(status_code=404, detail="Concepto de evaluación no encontrado")
    
    db_concepto.aprobado = True
    db_concepto.fecha_evaluacion = datetime.utcnow()
    if observaciones:
        db_concepto.observaciones = observaciones
    
    db.commit()
    db.refresh(db_concepto)
    return db_concepto

@router.get("/estado/{estado_id}", response_model=List[schemas.ConceptoEvaluacion])
def read_conceptos_evaluacion_by_estado(
    estado_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    conceptos = db.query(models.ConceptoEvaluacion).filter(
        models.ConceptoEvaluacion.estado_id == estado_id
    ).all()
    return conceptos

@router.get("/fecha/{fecha_inicio}/{fecha_fin}", response_model=List[schemas.ConceptoEvaluacion])
def read_conceptos_evaluacion_by_fecha(
    fecha_inicio: datetime,
    fecha_fin: datetime,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    conceptos = db.query(models.ConceptoEvaluacion).filter(
        and_(
            models.ConceptoEvaluacion.fecha_evaluacion >= fecha_inicio,
            models.ConceptoEvaluacion.fecha_evaluacion <= fecha_fin
        )
    ).all()
    return conceptos

@router.get("/estadisticas/", response_model=dict)
def get_estadisticas_evaluacion(
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    total_conceptos = db.query(models.ConceptoEvaluacion).count()
    conceptos_aprobados = db.query(models.ConceptoEvaluacion).filter(
        models.ConceptoEvaluacion.aprobado == True
    ).count()
    promedio_puntaje = db.query(func.avg(models.ConceptoEvaluacion.puntaje)).scalar() or 0
    
    return {
        "total_conceptos": total_conceptos,
        "conceptos_aprobados": conceptos_aprobados,
        "conceptos_pendientes": total_conceptos - conceptos_aprobados,
        "promedio_puntaje": round(promedio_puntaje, 2)
    }
