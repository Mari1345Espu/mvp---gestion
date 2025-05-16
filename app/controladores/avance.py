from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import esquemas, modelos
from app.db.session import get_db
from app.esquemas.avance import Avance, AvanceCreate, AvanceBase
from app.modelos.avance import Avance

router = APIRouter()

@router.get("/avances/", response_model=List[esquemas.Avance])
def leer_avances(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    avances = db.query(modelos.Avance).offset(skip).limit(limit).all()
    return avances

@router.get("/avances/{avance_id}", response_model=esquemas.Avance)
def leer_avance(avance_id: int, db: Session = Depends(get_db)):
    avance = db.query(modelos.Avance).filter(modelos.Avance.id == avance_id).first()
    if avance is None:
        raise HTTPException(status_code=404, detail="Avance no encontrado")
    return avance

@router.post("/avances/", response_model=esquemas.Avance)
def crear_avance(avance: esquemas.AvanceCreate, db: Session = Depends(get_db)):
    db_avance = modelos.Avance(**avance.dict())
    db.add(db_avance)
    db.commit()
    db.refresh(db_avance)
    return db_avance

@router.put("/avances/{avance_id}", response_model=esquemas.Avance)
def actualizar_avance(avance_id: int, avance: esquemas.AvanceCreate, db: Session = Depends(get_db)):
    db_avance = db.query(modelos.Avance).filter(modelos.Avance.id == avance_id).first()
    if db_avance is None:
        raise HTTPException(status_code=404, detail="Avance no encontrado")
    for key, value in avance.dict().items():
        setattr(db_avance, key, value)
    db.commit()
    db.refresh(db_avance)
    return db_avance

@router.delete("/avances/{avance_id}", response_model=esquemas.Avance)
def eliminar_avance(avance_id: int, db: Session = Depends(get_db)):
    db_avance = db.query(modelos.Avance).filter(modelos.Avance.id == avance_id).first()
    if db_avance is None:
        raise HTTPException(status_code=404, detail="Avance no encontrado")
    db.delete(db_avance)
    db.commit()
    return db_avance
