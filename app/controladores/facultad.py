from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import esquemas, modelos
from app.db.session import get_db

from app.esquemas.facultad import FacultadBase, FacultadCreate, Facultad
from app.modelos.facultad import Facultad as FacultadModelo

router = APIRouter()

@router.get("/facultades/", response_model=List[esquemas.Facultad])
def leer_facultades(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    facultades = db.query(modelos.Facultad).offset(skip).limit(limit).all()
    return facultades

@router.get("/facultades/{facultad_id}", response_model=esquemas.Facultad)
def leer_facultad(facultad_id: int, db: Session = Depends(get_db)):
    facultad = db.query(modelos.Facultad).filter(modelos.Facultad.id == facultad_id).first()
    if facultad is None:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")
    return facultad

@router.post("/facultades/", response_model=esquemas.Facultad)
def crear_facultad(facultad: esquemas.FacultadCreate, db: Session = Depends(get_db)):
    db_facultad = modelos.Facultad(**facultad.dict())
    db.add(db_facultad)
    db.commit()
    db.refresh(db_facultad)
    return db_facultad

@router.put("/facultades/{facultad_id}", response_model=esquemas.Facultad)
def actualizar_facultad(facultad_id: int, facultad: esquemas.FacultadCreate, db: Session = Depends(get_db)):
    db_facultad = db.query(modelos.Facultad).filter(modelos.Facultad.id == facultad_id).first()
    if db_facultad is None:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")
    for key, value in facultad.dict().items():
        setattr(db_facultad, key, value)
    db.commit()
    db.refresh(db_facultad)
    return db_facultad

@router.delete("/facultades/{facultad_id}", response_model=esquemas.Facultad)
def eliminar_facultad(facultad_id: int, db: Session = Depends(get_db)):
    db_facultad = db.query(modelos.Facultad).filter(modelos.Facultad.id == facultad_id).first()
    if db_facultad is None:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")
    db.delete(db_facultad)
    db.commit()
    return db_facultad
