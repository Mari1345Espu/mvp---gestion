from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import esquemas, modelos
from app.db.session import get_db

from app.esquemas.evaluacion import EvaluacionBase, EvaluacionCreate, Evaluacion
from app.modelos.evaluacion import Evaluacion as EvaluacionModelo

router = APIRouter()

@router.get("/evaluaciones/", response_model=List[esquemas.Evaluacion])
def leer_evaluaciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    evaluaciones = db.query(modelos.Evaluacion).offset(skip).limit(limit).all()
    return evaluaciones

@router.get("/evaluaciones/{evaluacion_id}", response_model=esquemas.Evaluacion)
def leer_evaluacion(evaluacion_id: int, db: Session = Depends(get_db)):
    evaluacion = db.query(modelos.Evaluacion).filter(modelos.Evaluacion.id == evaluacion_id).first()
    if evaluacion is None:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    return evaluacion

@router.post("/evaluaciones/", response_model=esquemas.Evaluacion)
def crear_evaluacion(evaluacion: esquemas.EvaluacionCreate, db: Session = Depends(get_db)):
    db_evaluacion = modelos.Evaluacion(**evaluacion.dict())
    db.add(db_evaluacion)
    db.commit()
    db.refresh(db_evaluacion)
    return db_evaluacion

@router.put("/evaluaciones/{evaluacion_id}", response_model=esquemas.Evaluacion)
def actualizar_evaluacion(evaluacion_id: int, evaluacion: esquemas.EvaluacionCreate, db: Session = Depends(get_db)):
    db_evaluacion = db.query(modelos.Evaluacion).filter(modelos.Evaluacion.id == evaluacion_id).first()
    if db_evaluacion is None:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    for key, value in evaluacion.dict().items():
        setattr(db_evaluacion, key, value)
    db.commit()
    db.refresh(db_evaluacion)
    return db_evaluacion

@router.delete("/evaluaciones/{evaluacion_id}", response_model=esquemas.Evaluacion)
def eliminar_evaluacion(evaluacion_id: int, db: Session = Depends(get_db)):
    db_evaluacion = db.query(modelos.Evaluacion).filter(modelos.Evaluacion.id == evaluacion_id).first()
    if db_evaluacion is None:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    db.delete(db_evaluacion)
    db.commit()
    return db_evaluacion
