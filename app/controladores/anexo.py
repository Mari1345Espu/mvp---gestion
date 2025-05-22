from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional
from datetime import datetime
import os
import shutil
from pathlib import Path

from app import modelos
from app.db.session import get_db
from app.esquemas.anexo import (
    Anexo as AnexoSchema,
    AnexoCreate,
    AnexoUpdate,
    AnexoEstadisticas
)
from app.core.seguridad import get_current_user

router = APIRouter(
    prefix="/anexos",
    tags=["anexos"]
)

# Configuración de directorios
UPLOAD_DIR = Path("uploads/anexos")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.get("/", response_model=List[AnexoSchema])
def read_anexos(
    skip: int = 0,
    limit: int = 100,
    tipo_anexo_id: Optional[int] = None,
    proyecto_id: Optional[int] = None,
    producto_id: Optional[int] = None,
    convocatoria_id: Optional[int] = None,
    estado_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    query = db.query(modelos.Anexo)
    
    if tipo_anexo_id:
        query = query.filter(modelos.Anexo.tipo_anexo_id == tipo_anexo_id)
    if proyecto_id:
        query = query.filter(modelos.Anexo.proyecto_id == proyecto_id)
    if producto_id:
        query = query.filter(modelos.Anexo.producto_id == producto_id)
    if convocatoria_id:
        query = query.filter(modelos.Anexo.convocatoria_id == convocatoria_id)
    if estado_id:
        query = query.filter(modelos.Anexo.estado_id == estado_id)
    if search:
        query = query.filter(
            or_(
                modelos.Anexo.nombre.ilike(f"%{search}%"),
                modelos.Anexo.descripcion.ilike(f"%{search}%")
            )
        )
    
    anexos = query.offset(skip).limit(limit).all()
    return anexos

@router.get("/{anexo_id}", response_model=AnexoSchema)
def read_anexo(
    anexo_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    anexo = db.query(modelos.Anexo).filter(
        modelos.Anexo.id == anexo_id
    ).first()
    if anexo is None:
        raise HTTPException(status_code=404, detail="Anexo no encontrado")
    return anexo

@router.post("/", response_model=AnexoSchema)
async def create_anexo(
    archivo: UploadFile = File(...),
    nombre: str = None,
    descripcion: Optional[str] = None,
    tipo_anexo_id: int = None,
    proyecto_id: Optional[int] = None,
    producto_id: Optional[int] = None,
    convocatoria_id: Optional[int] = None,
    observaciones: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre not in ["Admin", "Investigador"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para subir anexos"
        )
    
    # Validar que al menos uno de los IDs esté presente
    if not any([proyecto_id, producto_id, convocatoria_id]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe especificar al menos un proyecto, producto o convocatoria"
        )
    
    # Generar nombre único para el archivo
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    extension = os.path.splitext(archivo.filename)[1]
    nombre_archivo = f"{timestamp}_{archivo.filename}"
    ruta_archivo = UPLOAD_DIR / nombre_archivo
    
    # Guardar archivo
    try:
        with open(ruta_archivo, "wb") as buffer:
            shutil.copyfileobj(archivo.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al guardar el archivo: {str(e)}"
        )
    
    # Crear anexo en la base de datos
    db_anexo = modelos.Anexo(
        nombre=nombre or archivo.filename,
        descripcion=descripcion,
        tipo_anexo_id=tipo_anexo_id,
        proyecto_id=proyecto_id,
        producto_id=producto_id,
        convocatoria_id=convocatoria_id,
        archivo=str(ruta_archivo),
        observaciones=observaciones,
        fecha_subida=datetime.utcnow(),
        subido_por_id=current_user.id,
        tamanio=os.path.getsize(ruta_archivo),
        tipo_archivo=extension[1:].lower()
    )
    
    db.add(db_anexo)
    db.commit()
    db.refresh(db_anexo)
    return db_anexo

@router.put("/{anexo_id}", response_model=AnexoSchema)
def update_anexo(
    anexo_id: int,
    anexo: AnexoUpdate,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre not in ["Admin", "Investigador"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para actualizar anexos"
        )
    
    db_anexo = db.query(modelos.Anexo).filter(
        modelos.Anexo.id == anexo_id
    ).first()
    if db_anexo is None:
        raise HTTPException(status_code=404, detail="Anexo no encontrado")
    
    # Verificar permisos específicos
    if current_user.rol.nombre != "Admin" and db_anexo.subido_por_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo puede actualizar sus propios anexos"
        )
    
    # Actualizar campos
    for key, value in anexo.dict(exclude_unset=True).items():
        setattr(db_anexo, key, value)
    
    db_anexo.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_anexo)
    return db_anexo

@router.delete("/{anexo_id}", response_model=AnexoSchema)
def delete_anexo(
    anexo_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden eliminar anexos"
        )
    
    db_anexo = db.query(modelos.Anexo).filter(
        modelos.Anexo.id == anexo_id
    ).first()
    if db_anexo is None:
        raise HTTPException(status_code=404, detail="Anexo no encontrado")
    
    # Eliminar archivo físico
    try:
        if os.path.exists(db_anexo.archivo):
            os.remove(db_anexo.archivo)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el archivo: {str(e)}"
        )
    
    db.delete(db_anexo)
    db.commit()
    return db_anexo

@router.get("/estadisticas/", response_model=AnexoEstadisticas)
def get_estadisticas_anexos(
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden ver las estadísticas"
        )
    
    # Total de anexos
    total_anexos = db.query(func.count(modelos.Anexo.id)).scalar()
    
    # Anexos por tipo
    anexos_por_tipo = dict(
        db.query(
            modelos.TipoAnexo.nombre,
            func.count(modelos.Anexo.id)
        ).join(modelos.Anexo).group_by(modelos.TipoAnexo.nombre).all()
    )
    
    # Anexos por estado
    anexos_por_estado = dict(
        db.query(
            modelos.Estado.nombre,
            func.count(modelos.Anexo.id)
        ).join(modelos.Anexo).group_by(modelos.Estado.nombre).all()
    )
    
    # Anexos por tipo de estado
    anexos_por_tipo_estado = dict(
        db.query(
            modelos.TipoEstado.nombre,
            func.count(modelos.Anexo.id)
        ).join(modelos.Anexo).group_by(modelos.TipoEstado.nombre).all()
    )
    
    # Anexos por proyecto
    anexos_por_proyecto = dict(
        db.query(
            modelos.Proyecto.nombre,
            func.count(modelos.Anexo.id)
        ).join(modelos.Anexo).group_by(modelos.Proyecto.nombre).all()
    )
    
    # Anexos por producto
    anexos_por_producto = dict(
        db.query(
            modelos.Producto.nombre,
            func.count(modelos.Anexo.id)
        ).join(modelos.Anexo).group_by(modelos.Producto.nombre).all()
    )
    
    # Anexos por convocatoria
    anexos_por_convocatoria = dict(
        db.query(
            modelos.Convocatoria.nombre,
            func.count(modelos.Anexo.id)
        ).join(modelos.Anexo).group_by(modelos.Convocatoria.nombre).all()
    )
    
    # Anexos por mes
    anexos_por_mes = dict(
        db.query(
            func.date_trunc('month', modelos.Anexo.fecha_creacion).label('mes'),
            func.count(modelos.Anexo.id)
        ).group_by('mes').all()
    )
    
    # Estadísticas de tamaño
    anexos = db.query(modelos.Anexo).all()
    total_espacio = sum(anexo.tamanio or 0 for anexo in anexos)
    promedio_tamanio = total_espacio / total_anexos if total_anexos > 0 else 0
    
    # Anexos por tipo de archivo
    anexos_por_tipo_archivo = dict(
        db.query(
            modelos.Anexo.tipo_archivo,
            func.count(modelos.Anexo.id)
        ).group_by(modelos.Anexo.tipo_archivo).all()
    )
    
    return AnexoEstadisticas(
        total_anexos=total_anexos,
        anexos_por_tipo=anexos_por_tipo,
        anexos_por_estado=anexos_por_estado,
        anexos_por_tipo_estado=anexos_por_tipo_estado,
        anexos_por_proyecto=anexos_por_proyecto,
        anexos_por_producto=anexos_por_producto,
        anexos_por_convocatoria=anexos_por_convocatoria,
        anexos_por_mes=anexos_por_mes,
        promedio_tamanio=promedio_tamanio,
        total_espacio_ocupado=total_espacio,
        anexos_por_tipo_archivo=anexos_por_tipo_archivo
    )
