from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import esquemas, modelos
from app.db.session import get_db

from app.esquemas.tipo_proyecto import TipoProyectoBase, TipoProyectoCreate, TipoProyecto
from app.modelos.tipo_proyecto import TipoProyecto as TipoProyectoModelo

router = APIRouter()

@router.get("/tipos_proyecto/", response_model=List[esquemas.TipoProyecto])
def leer_tipos_proyecto(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tipos_proyecto = db.query(modelos.TipoProyecto).offset(skip).limit(limit).all()
    return tipos_proyecto

@router.get("/tipos_proyecto/{tipo_proyecto_id}", response_model=esquemas.TipoProyecto)
def leer_tipo_proyecto(tipo_proyecto_id: int, db: Session = Depends(get_db)):
    tipo_proyecto = db.query(modelos.TipoProyecto).filter(modelos.TipoProyecto.id == tipo_proyecto_id).first()
    if tipo_proyecto is None:
        raise HTTPException(status_code=404, detail="Tipo de proyecto no encontrado")
    return tipo_proyecto

@router.post("/tipos_proyecto/", response_model=esquemas.TipoProyecto)
def crear_tipo_proyecto(tipo_proyecto: esquemas.TipoProyectoCreate, db: Session = Depends(get_db)):
    db_tipo_proyecto = modelos.TipoProyecto(**tipo_proyecto.dict())
    db.add(db_tipo_proyecto)
    db.commit()
    db.refresh(db_tipo_proyecto)
    return db_tipo_proyecto

@router.put("/tipos_proyecto/{tipo_proyecto_id}", response_model=esquemas.TipoProyecto)
def actualizar_tipo_proyecto(tipo_proyecto_id: int, tipo_proyecto: esquemas.TipoProyectoCreate, db: Session = Depends(get_db)):
    db_tipo_proyecto = db.query(modelos.TipoProyecto).filter(modelos.TipoProyecto.id == tipo_proyecto_id).first()
    if db_tipo_proyecto is None:
        raise HTTPException(status_code=404, detail="Tipo de proyecto no encontrado")
    for key, value in tipo_proyecto.dict().items():
        setattr(db_tipo_proyecto, key, value)
    db.commit()
    db.refresh(db_tipo_proyecto)
    return db_tipo_proyecto

@router.delete("/tipos_proyecto/{tipo_proyecto_id}", response_model=esquemas.TipoProyecto)
def eliminar_tipo_proyecto(tipo_proyecto_id: int, db: Session = Depends(get_db)):
    db_tipo_proyecto = db.query(modelos.TipoProyecto).filter(modelos.TipoProyecto.id == tipo_proyecto_id).first()
    if db_tipo_proyecto is None:
        raise HTTPException(status_code=404, detail="Tipo de proyecto no encontrado")
    db.delete(db_tipo_proyecto)
    db.commit()
    return db_tipo_proyecto
