from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import esquemas, modelos
from app.db.session import get_db

from app.esquemas.extension import ExtensionBase, ExtensionCreate, Extension
from app.modelos.extension import Extension as ExtensionModelo

router = APIRouter()

@router.get("/extensiones/", response_model=List[esquemas.Extension])
def leer_extensiones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    extensiones = db.query(modelos.Extension).offset(skip).limit(limit).all()
    return extensiones

@router.get("/extensiones/{extension_id}", response_model=esquemas.Extension)
def leer_extension(extension_id: int, db: Session = Depends(get_db)):
    extension = db.query(modelos.Extension).filter(modelos.Extension.id == extension_id).first()
    if extension is None:
        raise HTTPException(status_code=404, detail="Extensión no encontrada")
    return extension

@router.post("/extensiones/", response_model=esquemas.Extension)
def crear_extension(extension: esquemas.ExtensionCreate, db: Session = Depends(get_db)):
    db_extension = modelos.Extension(**extension.dict())
    db.add(db_extension)
    db.commit()
    db.refresh(db_extension)
    return db_extension

@router.put("/extensiones/{extension_id}", response_model=esquemas.Extension)
def actualizar_extension(extension_id: int, extension: esquemas.ExtensionCreate, db: Session = Depends(get_db)):
    db_extension = db.query(modelos.Extension).filter(modelos.Extension.id == extension_id).first()
    if db_extension is None:
        raise HTTPException(status_code=404, detail="Extensión no encontrada")
    for key, value in extension.dict().items():
        setattr(db_extension, key, value)
    db.commit()
    db.refresh(db_extension)
    return db_extension

@router.delete("/extensiones/{extension_id}", response_model=esquemas.Extension)
def eliminar_extension(extension_id: int, db: Session = Depends(get_db)):
    db_extension = db.query(modelos.Extension).filter(modelos.Extension.id == extension_id).first()
    if db_extension is None:
        raise HTTPException(status_code=404, detail="Extensión no encontrada")
    db.delete(db_extension)
    db.commit()
    return db_extension
