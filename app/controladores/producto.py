from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import esquemas, modelos
from app.db.session import get_db
from app.esquemas.producto import ProductoCreate, Producto, ProductoBase
from app.esquemas.producto import ProductoBase, ProductoCreate, Producto
router = APIRouter()

@router.get("/productos/", response_model=List[esquemas.Producto])
def leer_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    productos = db.query(modelos.Producto).offset(skip).limit(limit).all()
    return productos

@router.get("/productos/{producto_id}", response_model=esquemas.Producto)
def leer_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(modelos.Producto).filter(modelos.Producto.id == producto_id).first()
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.post("/productos/", response_model=esquemas.Producto)
def crear_producto(producto: esquemas.ProductoCreate, db: Session = Depends(get_db)):
    db_producto = modelos.Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router.put("/productos/{producto_id}", response_model=esquemas.Producto)
def actualizar_producto(producto_id: int, producto: esquemas.ProductoCreate, db: Session = Depends(get_db)):
    db_producto = db.query(modelos.Producto).filter(modelos.Producto.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for key, value in producto.dict().items():
        setattr(db_producto, key, value)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router.delete("/productos/{producto_id}", response_model=esquemas.Producto)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = db.query(modelos.Producto).filter(modelos.Producto.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(db_producto)
    db.commit()
    return db_producto
