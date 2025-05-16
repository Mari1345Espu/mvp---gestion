from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import esquemas, modelos
from app.db.session import get_db
from app.esquemas.cronograma import CronogramaCreate, Cronograma, CronogramaBase
from app.modelos.cronograma import Cronograma as CronogramaModel


router = APIRouter()

@router.get("/cronogramas/", response_model=List[esquemas.Cronograma])
def leer_cronogramas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cronogramas = db.query(modelos.Cronograma).offset(skip).limit(limit).all()
    return cronogramas

@router.get("/cronogramas/{cronograma_id}", response_model=esquemas.Cronograma)
def leer_cronograma(cronograma_id: int, db: Session = Depends(get_db)):
    cronograma = db.query(modelos.Cronograma).filter(modelos.Cronograma.id == cronograma_id).first()
    if cronograma is None:
        raise HTTPException(status_code=404, detail="Cronograma no encontrado")
    return cronograma

@router.post("/cronogramas/", response_model=esquemas.Cronograma)
def crear_cronograma(cronograma: esquemas.CronogramaCreate, db: Session = Depends(get_db)):
    db_cronograma = modelos.Cronograma(**cronograma.dict())
    db.add(db_cronograma)
    db.commit()
    db.refresh(db_cronograma)
    return db_cronograma

@router.put("/cronogramas/{cronograma_id}", response_model=esquemas.Cronograma)
def actualizar_cronograma(cronograma_id: int, cronograma: esquemas.CronogramaCreate, db: Session = Depends(get_db)):
    db_cronograma = db.query(modelos.Cronograma).filter(modelos.Cronograma.id == cronograma_id).first()
    if db_cronograma is None:
        raise HTTPException(status_code=404, detail="Cronograma no encontrado")
    for key, value in cronograma.dict().items():
        setattr(db_cronograma, key, value)
    db.commit()
    db.refresh(db_cronograma)
    return db_cronograma

@router.delete("/cronogramas/{cronograma_id}", response_model=esquemas.Cronograma)
def eliminar_cronograma(cronograma_id: int, db: Session = Depends(get_db)):
    db_cronograma = db.query(modelos.Cronograma).filter(modelos.Cronograma.id == cronograma_id).first()
    if db_cronograma is None:
        raise HTTPException(status_code=404, detail="Cronograma no encontrado")
    db.delete(db_cronograma)
    db.commit()
    return db_cronograma
