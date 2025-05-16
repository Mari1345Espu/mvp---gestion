from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import esquemas, modelos
from app.db.session import get_db

from app.esquemas.grupoinvestigacion import GrupoInvestigacionBase, GrupoInvestigacionCreate, GrupoInvestigacion
from app.modelos.grupoinvestigacion import GrupoInvestigacion as GrupoInvestigacionModelo

router = APIRouter()

@router.get("/grupos_investigacion/", response_model=List[esquemas.GrupoInvestigacion])
def leer_grupos_investigacion(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    grupos = db.query(modelos.GrupoInvestigacion).offset(skip).limit(limit).all()
    return grupos

@router.get("/grupos_investigacion/{grupo_id}", response_model=esquemas.GrupoInvestigacion)
def leer_grupo_investigacion(grupo_id: int, db: Session = Depends(get_db)):
    grupo = db.query(modelos.GrupoInvestigacion).filter(modelos.GrupoInvestigacion.id == grupo_id).first()
    if grupo is None:
        raise HTTPException(status_code=404, detail="Grupo de investigación no encontrado")
    return grupo

@router.post("/grupos_investigacion/", response_model=esquemas.GrupoInvestigacion)
def crear_grupo_investigacion(grupo: esquemas.GrupoInvestigacionCreate, db: Session = Depends(get_db)):
    db_grupo = modelos.GrupoInvestigacion(**grupo.dict())
    db.add(db_grupo)
    db.commit()
    db.refresh(db_grupo)
    return db_grupo

@router.put("/grupos_investigacion/{grupo_id}", response_model=esquemas.GrupoInvestigacion)
def actualizar_grupo_investigacion(grupo_id: int, grupo: esquemas.GrupoInvestigacionCreate, db: Session = Depends(get_db)):
    db_grupo = db.query(modelos.GrupoInvestigacion).filter(modelos.GrupoInvestigacion.id == grupo_id).first()
    if db_grupo is None:
        raise HTTPException(status_code=404, detail="Grupo de investigación no encontrado")
    for key, value in grupo.dict().items():
        setattr(db_grupo, key, value)
    db.commit()
    db.refresh(db_grupo)
    return db_grupo

@router.delete("/grupos_investigacion/{grupo_id}", response_model=esquemas.GrupoInvestigacion)
def eliminar_grupo_investigacion(grupo_id: int, db: Session = Depends(get_db)):
    db_grupo = db.query(modelos.GrupoInvestigacion).filter(modelos.GrupoInvestigacion.id == grupo_id).first()
    if db_grupo is None:
        raise HTTPException(status_code=404, detail="Grupo de investigación no encontrado")
    db.delete(db_grupo)
    db.commit()
    return db_grupo
