from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import esquemas, modelos
from app.db.session import get_db

from app.esquemas.convocatoria import ConvocatoriaBase, ConvocatoriaCreate, Convocatoria
from app.modelos.convocatoria import Convocatoria as ConvocatoriaModelo

router = APIRouter()

@router.get("/convocatorias/", response_model=List[esquemas.Convocatoria])
def leer_convocatorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    convocatorias = db.query(modelos.Convocatoria).offset(skip).limit(limit).all()
    return convocatorias

@router.get("/convocatorias/{convocatoria_id}", response_model=esquemas.Convocatoria)
def leer_convocatoria(convocatoria_id: int, db: Session = Depends(get_db)):
    convocatoria = db.query(modelos.Convocatoria).filter(modelos.Convocatoria.id == convocatoria_id).first()
    if convocatoria is None:
        raise HTTPException(status_code=404, detail="Convocatoria no encontrada")
    return convocatoria

@router.post("/convocatorias/", response_model=esquemas.Convocatoria)
def crear_convocatoria(convocatoria: esquemas.ConvocatoriaCreate, db: Session = Depends(get_db)):
    db_convocatoria = modelos.Convocatoria(**convocatoria.dict())
    db.add(db_convocatoria)
    db.commit()
    db.refresh(db_convocatoria)
    return db_convocatoria

@router.put("/convocatorias/{convocatoria_id}", response_model=esquemas.Convocatoria)
def actualizar_convocatoria(convocatoria_id: int, convocatoria: esquemas.ConvocatoriaCreate, db: Session = Depends(get_db)):
    db_convocatoria = db.query(modelos.Convocatoria).filter(modelos.Convocatoria.id == convocatoria_id).first()
    if db_convocatoria is None:
        raise HTTPException(status_code=404, detail="Convocatoria no encontrada")
    for key, value in convocatoria.dict().items():
        setattr(db_convocatoria, key, value)
    db.commit()
    db.refresh(db_convocatoria)
    return db_convocatoria

@router.delete("/convocatorias/{convocatoria_id}", response_model=esquemas.Convocatoria)
def eliminar_convocatoria(convocatoria_id: int, db: Session = Depends(get_db)):
    db_convocatoria = db.query(modelos.Convocatoria).filter(modelos.Convocatoria.id == convocatoria_id).first()
    if db_convocatoria is None:
        raise HTTPException(status_code=404, detail="Convocatoria no encontrada")
    db.delete(db_convocatoria)
    db.commit()
    return db_convocatoria
