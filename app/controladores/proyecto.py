from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import esquemas, modelos
from app.db.session import get_db
from app.esquemas.proyecto import Proyecto, ProyectoCreate, ProyectoBase
from app.modelos.proyecto import Proyecto

router = APIRouter()

@router.get("/proyectos/", response_model=List[esquemas.Proyecto])
def leer_proyectos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    proyectos = db.query(modelos.Proyecto).offset(skip).limit(limit).all()
    return proyectos

@router.get("/proyectos/{proyecto_id}", response_model=esquemas.Proyecto)
def leer_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    proyecto = db.query(modelos.Proyecto).filter(modelos.Proyecto.id == proyecto_id).first()
    if proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return proyecto

@router.post("/proyectos/", response_model=esquemas.Proyecto)
def crear_proyecto(proyecto: esquemas.ProyectoCreate, db: Session = Depends(get_db)):
    db_proyecto = modelos.Proyecto(**proyecto.dict())
    db.add(db_proyecto)
    db.commit()
    db.refresh(db_proyecto)
    return db_proyecto

@router.put("/proyectos/{proyecto_id}", response_model=esquemas.Proyecto)
def actualizar_proyecto(proyecto_id: int, proyecto: esquemas.ProyectoCreate, db: Session = Depends(get_db)):
    db_proyecto = db.query(modelos.Proyecto).filter(modelos.Proyecto.id == proyecto_id).first()
    if db_proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    for key, value in proyecto.dict().items():
        setattr(db_proyecto, key, value)
    db.commit()
    db.refresh(db_proyecto)
    return db_proyecto

@router.delete("/proyectos/{proyecto_id}", response_model=esquemas.Proyecto)
def eliminar_proyecto(proyecto_id: int, db: Session = Depends(get_db)):
    db_proyecto = db.query(modelos.Proyecto).filter(modelos.Proyecto.id == proyecto_id).first()
    if db_proyecto is None:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    db.delete(db_proyecto)
    db.commit()
    return db_proyecto
