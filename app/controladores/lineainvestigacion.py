from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import esquemas, modelos
from app.db.session import get_db

from app.esquemas.lineainvestigacion import LineaInvestigacionBase, LineaInvestigacionCreate, LineaInvestigacion
from app.modelos.lineainvestigacion import LineaInvestigacion as LineaInvestigacionModelo

router = APIRouter()

@router.get("/lineas_investigacion/", response_model=List[esquemas.LineaInvestigacion])
def leer_lineas_investigacion(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    lineas = db.query(modelos.LineaInvestigacion).offset(skip).limit(limit).all()
    return lineas

@router.get("/lineas_investigacion/{linea_id}", response_model=esquemas.LineaInvestigacion)
def leer_linea_investigacion(linea_id: int, db: Session = Depends(get_db)):
    linea = db.query(modelos.LineaInvestigacion).filter(modelos.LineaInvestigacion.id == linea_id).first()
    if linea is None:
        raise HTTPException(status_code=404, detail="Línea de investigación no encontrada")
    return linea

@router.post("/lineas_investigacion/", response_model=esquemas.LineaInvestigacion)
def crear_linea_investigacion(linea: esquemas.LineaInvestigacionCreate, db: Session = Depends(get_db)):
    db_linea = modelos.LineaInvestigacion(**linea.dict())
    db.add(db_linea)
    db.commit()
    db.refresh(db_linea)
    return db_linea

@router.put("/lineas_investigacion/{linea_id}", response_model=esquemas.LineaInvestigacion)
def actualizar_linea_investigacion(linea_id: int, linea: esquemas.LineaInvestigacionCreate, db: Session = Depends(get_db)):
    db_linea = db.query(modelos.LineaInvestigacion).filter(modelos.LineaInvestigacion.id == linea_id).first()
    if db_linea is None:
        raise HTTPException(status_code=404, detail="Línea de investigación no encontrada")
    for key, value in linea.dict().items():
        setattr(db_linea, key, value)
    db.commit()
    db.refresh(db_linea)
    return db_linea

@router.delete("/lineas_investigacion/{linea_id}", response_model=esquemas.LineaInvestigacion)
def eliminar_linea_investigacion(linea_id: int, db: Session = Depends(get_db)):
    db_linea = db.query(modelos.LineaInvestigacion).filter(modelos.LineaInvestigacion.id == linea_id).first()
    if db_linea is None:
        raise HTTPException(status_code=404, detail="Línea de investigación no encontrada")
    db.delete(db_linea)
    db.commit()
    return db_linea
