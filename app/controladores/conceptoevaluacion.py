from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import esquemas, modelos
from app.db.session import get_db

from app.esquemas.conceptoevaluacion import ConceptoEvaluacionCreate, ConceptoEvaluacion, ConceptoEvaluacionBase
from app.esquemas.conceptoevaluacion import ConceptoEvaluacionBase, ConceptoEvaluacionCreate, ConceptoEvaluacion

router = APIRouter()

@router.get("/conceptos_evaluacion/", response_model=List[esquemas.ConceptoEvaluacion])
def leer_conceptos_evaluacion(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    conceptos_evaluacion = db.query(modelos.ConceptoEvaluacion).offset(skip).limit(limit).all()
    return conceptos_evaluacion

@router.get("/conceptos_evaluacion/{concepto_evaluacion_id}", response_model=esquemas.ConceptoEvaluacion)
def leer_concepto_evaluacion(concepto_evaluacion_id: int, db: Session = Depends(get_db)):
    concepto_evaluacion = db.query(modelos.ConceptoEvaluacion).filter(modelos.ConceptoEvaluacion.id == concepto_evaluacion_id).first()
    if concepto_evaluacion is None:
        raise HTTPException(status_code=404, detail="Concepto de evaluación no encontrado")
    return concepto_evaluacion

@router.post("/conceptos_evaluacion/", response_model=esquemas.ConceptoEvaluacion)
def crear_concepto_evaluacion(concepto_evaluacion: esquemas.ConceptoEvaluacionCreate, db: Session = Depends(get_db)):
    db_concepto_evaluacion = modelos.ConceptoEvaluacion(**concepto_evaluacion.dict())
    db.add(db_concepto_evaluacion)
    db.commit()
    db.refresh(db_concepto_evaluacion)
    return db_concepto_evaluacion

@router.put("/conceptos_evaluacion/{concepto_evaluacion_id}", response_model=esquemas.ConceptoEvaluacion)
def actualizar_concepto_evaluacion(concepto_evaluacion_id: int, concepto_evaluacion: esquemas.ConceptoEvaluacionCreate, db: Session = Depends(get_db)):
    db_concepto_evaluacion = db.query(modelos.ConceptoEvaluacion).filter(modelos.ConceptoEvaluacion.id == concepto_evaluacion_id).first()
    if db_concepto_evaluacion is None:
        raise HTTPException(status_code=404, detail="Concepto de evaluación no encontrado")
    for key, value in concepto_evaluacion.dict().items():
        setattr(db_concepto_evaluacion, key, value)
    db.commit()
    db.refresh(db_concepto_evaluacion)
    return db_concepto_evaluacion

@router.delete("/conceptos_evaluacion/{concepto_evaluacion_id}", response_model=esquemas.ConceptoEvaluacion)
def eliminar_concepto_evaluacion(concepto_evaluacion_id: int, db: Session = Depends(get_db)):
    db_concepto_evaluacion = db.query(modelos.ConceptoEvaluacion).filter(modelos.ConceptoEvaluacion.id == concepto_evaluacion_id).first()
    if db_concepto_evaluacion is None:
        raise HTTPException(status_code=404, detail="Concepto de evaluación no encontrado")
    db.delete(db_concepto_evaluacion)
    db.commit()
    return db_concepto_evaluacion
