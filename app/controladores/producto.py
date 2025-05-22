from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile, Form, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional
from datetime import datetime, timedelta
import os

from app import esquemas, modelos
from app.db.session import get_db
from app.esquemas.producto import Producto as ProductoSchema, ProductoCreate, ProductoUpdate, ProductoEstadisticas
from app.core.seguridad import get_current_user

router = APIRouter(
    prefix="/productos",
    tags=["productos"]
)

@router.get("/", response_model=List[ProductoSchema])
def read_productos(
    skip: int = 0,
    limit: int = 100,
    tipo_producto_id: Optional[int] = None,
    proyecto_id: Optional[int] = None,
    estado_id: Optional[int] = None,
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    query = db.query(modelos.Producto)
    
    if tipo_producto_id:
        query = query.filter(modelos.Producto.tipo_producto_id == tipo_producto_id)
    if proyecto_id:
        query = query.filter(modelos.Producto.proyecto_id == proyecto_id)
    if estado_id:
        query = query.filter(modelos.Producto.estado_id == estado_id)
    if fecha_inicio and fecha_fin:
        query = query.filter(
            and_(
                modelos.Producto.fecha_creacion >= fecha_inicio,
                modelos.Producto.fecha_creacion <= fecha_fin
            )
        )
    if search:
        query = query.filter(
            or_(
                modelos.Producto.titulo.ilike(f"%{search}%"),
                modelos.Producto.descripcion.ilike(f"%{search}%"),
                modelos.Producto.palabras_clave.ilike(f"%{search}%")
            )
        )
    
    productos = query.offset(skip).limit(limit).all()
    return productos

@router.get("/{producto_id}", response_model=ProductoSchema)
def read_producto(
    producto_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    producto = db.query(modelos.Producto).filter(modelos.Producto.id == producto_id).first()
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.post("/", response_model=ProductoSchema)
async def create_producto(
    titulo: str = Form(...),
    descripcion: str = Form(...),
    tipo_producto_id: int = Form(...),
    proyecto_id: int = Form(...),
    estado_id: int = Form(...),
    tipo_estado_id: int = Form(...),
    archivo: UploadFile = File(None),
    observaciones: Optional[str] = Form(None),
    url: Optional[str] = Form(None),
    doi: Optional[str] = Form(None),
    issn: Optional[str] = Form(None),
    isbn: Optional[str] = Form(None),
    revista: Optional[str] = Form(None),
    editorial: Optional[str] = Form(None),
    volumen: Optional[str] = Form(None),
    numero: Optional[str] = Form(None),
    pagina_inicio: Optional[int] = Form(None),
    pagina_fin: Optional[int] = Form(None),
    autores: Optional[str] = Form(None),
    palabras_clave: Optional[str] = Form(None),
    resumen: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    # Verificar que el usuario tenga permisos para crear productos
    if current_user.rol.nombre not in ["Admin", "Investigador"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para crear productos"
        )
    
    # Verificar que el proyecto existe
    proyecto = db.query(modelos.Proyecto).filter(modelos.Proyecto.id == proyecto_id).first()
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    # Manejar el archivo si se proporciona
    archivo_url = None
    if archivo:
        uploads_dir = os.path.join("app", "static", "uploads", "productos")
        os.makedirs(uploads_dir, exist_ok=True)
        file_ext = os.path.splitext(archivo.filename)[1]
        file_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{archivo.filename}"
        file_path = os.path.join(uploads_dir, file_name)
        with open(file_path, "wb") as f:
            f.write(await archivo.read())
        archivo_url = f"/static/uploads/productos/{file_name}"
    
    db_producto = modelos.Producto(
        titulo=titulo,
        descripcion=descripcion,
        tipo_producto_id=tipo_producto_id,
        proyecto_id=proyecto_id,
        estado_id=estado_id,
        tipo_estado_id=tipo_estado_id,
        observaciones=observaciones,
        url=url,
        doi=doi,
        issn=issn,
        isbn=isbn,
        revista=revista,
        editorial=editorial,
        volumen=volumen,
        numero=numero,
        pagina_inicio=pagina_inicio,
        pagina_fin=pagina_fin,
        autores=autores,
        palabras_clave=palabras_clave,
        resumen=resumen,
        archivo=archivo_url
    )
    
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router.put("/{producto_id}", response_model=ProductoSchema)
async def update_producto(
    producto_id: int,
    titulo: Optional[str] = Form(None),
    descripcion: Optional[str] = Form(None),
    tipo_producto_id: Optional[int] = Form(None),
    estado_id: Optional[int] = Form(None),
    tipo_estado_id: Optional[int] = Form(None),
    archivo: Optional[UploadFile] = File(None),
    observaciones: Optional[str] = Form(None),
    url: Optional[str] = Form(None),
    doi: Optional[str] = Form(None),
    issn: Optional[str] = Form(None),
    isbn: Optional[str] = Form(None),
    revista: Optional[str] = Form(None),
    editorial: Optional[str] = Form(None),
    volumen: Optional[str] = Form(None),
    numero: Optional[str] = Form(None),
    pagina_inicio: Optional[int] = Form(None),
    pagina_fin: Optional[int] = Form(None),
    autores: Optional[str] = Form(None),
    palabras_clave: Optional[str] = Form(None),
    resumen: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    db_producto = db.query(modelos.Producto).filter(modelos.Producto.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Verificar permisos
    if current_user.rol.nombre not in ["Admin", "Investigador"] and current_user.id != db_producto.aprobado_por_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para actualizar este producto"
        )
    
    # Manejar el archivo si se proporciona
    if archivo:
        uploads_dir = os.path.join("app", "static", "uploads", "productos")
        os.makedirs(uploads_dir, exist_ok=True)
        file_ext = os.path.splitext(archivo.filename)[1]
        file_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{archivo.filename}"
        file_path = os.path.join(uploads_dir, file_name)
        with open(file_path, "wb") as f:
            f.write(await archivo.read())
        db_producto.archivo = f"/static/uploads/productos/{file_name}"
    
    # Actualizar campos
    if titulo is not None:
        db_producto.titulo = titulo
    if descripcion is not None:
        db_producto.descripcion = descripcion
    if tipo_producto_id is not None:
        db_producto.tipo_producto_id = tipo_producto_id
    if estado_id is not None:
        db_producto.estado_id = estado_id
    if tipo_estado_id is not None:
        db_producto.tipo_estado_id = tipo_estado_id
    if observaciones is not None:
        db_producto.observaciones = observaciones
    if url is not None:
        db_producto.url = url
    if doi is not None:
        db_producto.doi = doi
    if issn is not None:
        db_producto.issn = issn
    if isbn is not None:
        db_producto.isbn = isbn
    if revista is not None:
        db_producto.revista = revista
    if editorial is not None:
        db_producto.editorial = editorial
    if volumen is not None:
        db_producto.volumen = volumen
    if numero is not None:
        db_producto.numero = numero
    if pagina_inicio is not None:
        db_producto.pagina_inicio = pagina_inicio
    if pagina_fin is not None:
        db_producto.pagina_fin = pagina_fin
    if autores is not None:
        db_producto.autores = autores
    if palabras_clave is not None:
        db_producto.palabras_clave = palabras_clave
    if resumen is not None:
        db_producto.resumen = resumen
    
    db_producto.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router.delete("/{producto_id}", response_model=ProductoSchema)
def delete_producto(
    producto_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden eliminar productos"
        )
    
    db_producto = db.query(modelos.Producto).filter(modelos.Producto.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Eliminar archivo si existe
    if db_producto.archivo:
        try:
            os.remove(os.path.join("app", db_producto.archivo.lstrip("/")))
        except:
            pass
    
    db.delete(db_producto)
    db.commit()
    return db_producto

@router.get("/estadisticas/", response_model=ProductoEstadisticas)
def get_estadisticas_productos(
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden ver las estadísticas"
        )
    
    # Total de productos
    total_productos = db.query(func.count(modelos.Producto.id)).scalar()
    
    # Productos por tipo
    productos_por_tipo = dict(
        db.query(
            modelos.TipoProducto.nombre,
            func.count(modelos.Producto.id)
        ).join(modelos.Producto).group_by(modelos.TipoProducto.nombre).all()
    )
    
    # Productos por estado
    productos_por_estado = dict(
        db.query(
            modelos.Estado.nombre,
            func.count(modelos.Producto.id)
        ).join(modelos.Producto).group_by(modelos.Estado.nombre).all()
    )
    
    # Productos por proyecto
    productos_por_proyecto = dict(
        db.query(
            modelos.Proyecto.titulo,
            func.count(modelos.Producto.id)
        ).join(modelos.Producto).group_by(modelos.Proyecto.titulo).all()
    )
    
    # Productos aprobados, pendientes y rechazados
    productos_aprobados = db.query(func.count(modelos.Producto.id)).filter(
        modelos.Producto.estado_id == 1  # Asumiendo que 1 es el ID del estado "Aprobado"
    ).scalar()
    
    productos_pendientes = db.query(func.count(modelos.Producto.id)).filter(
        modelos.Producto.estado_id == 2  # Asumiendo que 2 es el ID del estado "Pendiente"
    ).scalar()
    
    productos_rechazados = db.query(func.count(modelos.Producto.id)).filter(
        modelos.Producto.estado_id == 3  # Asumiendo que 3 es el ID del estado "Rechazado"
    ).scalar()
    
    # Promedio de tiempo de aprobación
    productos_aprobados_query = db.query(modelos.Producto).filter(
        and_(
            modelos.Producto.estado_id == 1,
            modelos.Producto.fecha_aprobacion.isnot(None)
        )
    ).all()
    
    tiempo_total = timedelta()
    for producto in productos_aprobados_query:
        tiempo_total += producto.fecha_aprobacion - producto.fecha_creacion
    
    promedio_tiempo_aprobacion = tiempo_total.total_seconds() / len(productos_aprobados_query) if productos_aprobados_query else 0
    
    # Productos por mes
    productos_por_mes = dict(
        db.query(
            func.date_trunc('month', modelos.Producto.fecha_creacion).label('mes'),
            func.count(modelos.Producto.id)
        ).group_by('mes').all()
    )
    
    return ProductoEstadisticas(
        total_productos=total_productos,
        productos_por_tipo=productos_por_tipo,
        productos_por_estado=productos_por_estado,
        productos_por_proyecto=productos_por_proyecto,
        productos_aprobados=productos_aprobados,
        productos_pendientes=productos_pendientes,
        productos_rechazados=productos_rechazados,
        promedio_tiempo_aprobacion=promedio_tiempo_aprobacion,
        productos_por_mes=productos_por_mes
    )

@router.put("/{producto_id}/aprobar", response_model=ProductoSchema)
def aprobar_producto(
    producto_id: int,
    observaciones: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre not in ["Admin", "Evaluador"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para aprobar productos"
        )
    
    db_producto = db.query(modelos.Producto).filter(modelos.Producto.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    db_producto.estado_id = 1  # Asumiendo que 1 es el ID del estado "Aprobado"
    db_producto.aprobado_por_id = current_user.id
    db_producto.fecha_aprobacion = datetime.utcnow()
    if observaciones:
        db_producto.observaciones = observaciones
    db_producto.fecha_actualizacion = datetime.utcnow()
    
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router.put("/{producto_id}/rechazar", response_model=ProductoSchema)
def rechazar_producto(
    producto_id: int,
    observaciones: str,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre not in ["Admin", "Evaluador"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para rechazar productos"
        )
    
    if not observaciones:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Las observaciones son obligatorias al rechazar un producto"
        )
    
    db_producto = db.query(modelos.Producto).filter(modelos.Producto.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    db_producto.estado_id = 3  # Asumiendo que 3 es el ID del estado "Rechazado"
    db_producto.aprobado_por_id = current_user.id
    db_producto.fecha_aprobacion = datetime.utcnow()
    db_producto.observaciones = observaciones
    db_producto.fecha_actualizacion = datetime.utcnow()
    
    db.commit()
    db.refresh(db_producto)
    return db_producto
