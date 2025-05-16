from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import esquemas, modelos
from app.db.session import get_db

from app.esquemas.cierre import CierreBase, CierreCreate, Cierre
from app.modelos.cierre import Cierre as CierreModelo

router = APIRouter()

@router.get("/cierres/", response_model=List[esquemas.Cierre])
def leer_cierres(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cierres = db.query(modelos.Cierre).offset(skip).limit(limit).all()
    return cierres

@router.get("/cierres/{cierre_id}", response_model=esquemas.Cierre)
def leer_cierre(cierre_id: int, db: Session = Depends(get_db)):
    cierre = db.query(modelos.Cierre).filter(modelos.Cierre.id == cierre_id).first()
    if cierre is None:
        raise HTTPException(status_code=404, detail="Cierre no encontrado")
    return cierre

@router.post("/cierres/", response_model=esquemas.Cierre)
def crear_cierre(cierre: esquemas.CierreCreate, db: Session = Depends(get_db)):
    db_cierre = modelos.Cierre(**cierre.dict())
    db.add(db_cierre)
    db.commit()
    db.refresh(db_cierre)
    return db_cierre

@router.put("/cierres/{cierre_id}", response_model=esquemas.Cierre)
def actualizar_cierre(cierre_id: int, cierre: esquemas.CierreCreate, db: Session = Depends(get_db)):
    db_cierre = db.query(modelos.Cierre).filter(modelos.Cierre.id == cierre_id).first()
    if db_cierre is None:
        raise HTTPException(status_code=404, detail="Cierre no encontrado")
    for key, value in cierre.dict().items():
        setattr(db_cierre, key, value)
    db.commit()
    db.refresh(db_cierre)
    return db_cierre

@router.delete("/cierres/{cierre_id}", response_model=esquemas.Cierre)
def eliminar_cierre(cierre_id: int, db: Session = Depends(get_db)):
    db_cierre = db.query(modelos.Cierre).filter(modelos.Cierre.id == cierre_id).first()
    if db_cierre is None:
        raise HTTPException(status_code=404, detail="Cierre no encontrado")
    db.delete(db_cierre)
    db.commit()
    return db_cierre
