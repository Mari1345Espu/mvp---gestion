from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import esquemas, modelos
from app.db.session import get_db
from app.esquemas.tarea import TareaCreate, Tarea, TareaBase
from app.controladores.tarea import TareaBase, TareaCreate, Tarea

router = APIRouter()

@router.get("/tareas/", response_model=List[esquemas.Tarea])
def leer_tareas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tareas = db.query(modelos.Tarea).offset(skip).limit(limit).all()
    return tareas

@router.get("/tareas/{tarea_id}", response_model=esquemas.Tarea)
def leer_tarea(tarea_id: int, db: Session = Depends(get_db)):
    tarea = db.query(modelos.Tarea).filter(modelos.Tarea.id == tarea_id).first()
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea

@router.post("/tareas/", response_model=esquemas.Tarea)
def crear_tarea(tarea: esquemas.TareaCreate, db: Session = Depends(get_db)):
    db_tarea = modelos.Tarea(**tarea.dict())
    db.add(db_tarea)
    db.commit()
    db.refresh(db_tarea)
    return db_tarea

@router.put("/tareas/{tarea_id}", response_model=esquemas.Tarea)
def actualizar_tarea(tarea_id: int, tarea: esquemas.TareaCreate, db: Session = Depends(get_db)):
    db_tarea = db.query(modelos.Tarea).filter(modelos.Tarea.id == tarea_id).first()
    if db_tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    for key, value in tarea.dict().items():
        setattr(db_tarea, key, value)
    db.commit()
    db.refresh(db_tarea)
    return db_tarea

@router.delete("/tareas/{tarea_id}", response_model=esquemas.Tarea)
def eliminar_tarea(tarea_id: int, db: Session = Depends(get_db)):
    db_tarea = db.query(modelos.Tarea).filter(modelos.Tarea.id == tarea_id).first()
    if db_tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    db.delete(db_tarea)
    db.commit()
    return db_tarea
