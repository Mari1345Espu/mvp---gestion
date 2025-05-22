from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, extract
from typing import List, Optional
from datetime import datetime, timedelta
import os
import json

from app import modelos
from app.db.session import get_db
from app.esquemas.destino import (
    Destino as DestinoSchema,
    DestinoCreate,
    DestinoUpdate,
    DestinoEstadisticas
)
from app.core.seguridad import get_current_user

router = APIRouter(
    prefix="/destinos",
    tags=["destinos"]
)

# Configurar directorio para documentos
UPLOAD_DIR = "uploads/destinos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/", response_model=List[DestinoSchema])
def read_destinos(
    skip: int = 0,
    limit: int = 100,
    tipo_destino: Optional[str] = None,
    entidad_id: Optional[int] = None,
    responsable_id: Optional[int] = None,
    estado_id: Optional[int] = None,
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre not in ["Admin", "Investigador"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para ver los destinos"
        )
    
    query = db.query(modelos.Destino)
    
    if tipo_destino:
        query = query.filter(modelos.Destino.tipo_destino == tipo_destino)
    if entidad_id:
        query = query.filter(modelos.Destino.entidad_id == entidad_id)
    if responsable_id:
        query = query.filter(modelos.Destino.responsable_id == responsable_id)
    if estado_id:
        query = query.filter(modelos.Destino.estado_id == estado_id)
    if fecha_inicio and fecha_fin:
        query = query.filter(
            and_(
                modelos.Destino.fecha_destino >= fecha_inicio,
                modelos.Destino.fecha_destino <= fecha_fin
            )
        )
    if search:
        query = query.filter(
            or_(
                modelos.Destino.nombre.ilike(f"%{search}%"),
                modelos.Destino.descripcion.ilike(f"%{search}%"),
                modelos.Destino.observaciones.ilike(f"%{search}%")
            )
        )
    
    destinos = query.order_by(modelos.Destino.fecha_destino.desc()).offset(skip).limit(limit).all()
    return destinos

@router.get("/{destino_id}", response_model=DestinoSchema)
def read_destino(
    destino_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre not in ["Admin", "Investigador"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para ver los destinos"
        )
    
    destino = db.query(modelos.Destino).filter(
        modelos.Destino.id == destino_id
    ).first()
    if destino is None:
        raise HTTPException(status_code=404, detail="Destino no encontrado")
    return destino

@router.post("/", response_model=DestinoSchema)
def create_destino(
    destino: DestinoCreate,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre not in ["Admin", "Investigador"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para crear destinos"
        )
    
    # Verificar que la entidad existe
    if destino.tipo_destino == "proyecto":
        entidad = db.query(modelos.Proyecto).filter(
            modelos.Proyecto.id == destino.entidad_id
        ).first()
    else:  # convocatoria
        entidad = db.query(modelos.Convocatoria).filter(
            modelos.Convocatoria.id == destino.entidad_id
        ).first()
    
    if not entidad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La {destino.tipo_destino} especificada no existe"
        )
    
    # Verificar que no existe un destino previo
    destino_existente = db.query(modelos.Destino).filter(
        and_(
            modelos.Destino.tipo_destino == destino.tipo_destino,
            modelos.Destino.entidad_id == destino.entidad_id
        )
    ).first()
    
    if destino_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un destino para esta {destino.tipo_destino}"
        )
    
    db_destino = modelos.Destino(**destino.dict())
    db.add(db_destino)
    db.commit()
    db.refresh(db_destino)
    return db_destino

@router.put("/{destino_id}", response_model=DestinoSchema)
def update_destino(
    destino_id: int,
    destino: DestinoUpdate,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre not in ["Admin", "Investigador"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para actualizar destinos"
        )
    
    db_destino = db.query(modelos.Destino).filter(
        modelos.Destino.id == destino_id
    ).first()
    if db_destino is None:
        raise HTTPException(status_code=404, detail="Destino no encontrado")
    
    # Verificar permisos específicos
    if current_user.rol.nombre != "Admin" and db_destino.responsable_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo puede actualizar sus propios destinos"
        )
    
    # Actualizar campos
    for key, value in destino.dict(exclude_unset=True).items():
        setattr(db_destino, key, value)
    
    db_destino.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_destino)
    return db_destino

@router.delete("/{destino_id}", response_model=DestinoSchema)
def delete_destino(
    destino_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden eliminar destinos"
        )
    
    db_destino = db.query(modelos.Destino).filter(
        modelos.Destino.id == destino_id
    ).first()
    if db_destino is None:
        raise HTTPException(status_code=404, detail="Destino no encontrado")
    
    # Eliminar documentos asociados
    if db_destino.documentos:
        for doc in db_destino.documentos:
            try:
                os.remove(os.path.join(UPLOAD_DIR, doc))
            except:
                pass
    
    db.delete(db_destino)
    db.commit()
    return db_destino

@router.post("/{destino_id}/documentos")
async def upload_documento(
    destino_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre not in ["Admin", "Investigador"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para subir documentos"
        )
    
    db_destino = db.query(modelos.Destino).filter(
        modelos.Destino.id == destino_id
    ).first()
    if db_destino is None:
        raise HTTPException(status_code=404, detail="Destino no encontrado")
    
    # Generar nombre único para el archivo
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"{destino_id}_{timestamp}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    # Guardar archivo
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Actualizar lista de documentos
    documentos = db_destino.documentos or []
    documentos.append(filename)
    db_destino.documentos = documentos
    db_destino.fecha_actualizacion = datetime.utcnow()
    
    db.commit()
    db.refresh(db_destino)
    return {"filename": filename}

@router.get("/estadisticas/", response_model=DestinoEstadisticas)
def get_estadisticas_destinos(
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden ver las estadísticas"
        )
    
    # Total de destinos
    total_destinos = db.query(func.count(modelos.Destino.id)).scalar()
    
    # Destinos por tipo
    destinos_por_tipo = dict(
        db.query(
            modelos.Destino.tipo_destino,
            func.count(modelos.Destino.id)
        ).group_by(modelos.Destino.tipo_destino).all()
    )
    
    # Destinos por estado
    destinos_por_estado = dict(
        db.query(
            modelos.Estado.nombre,
            func.count(modelos.Destino.id)
        ).join(modelos.Destino).group_by(modelos.Estado.nombre).all()
    )
    
    # Destinos por responsable
    destinos_por_responsable = dict(
        db.query(
            modelos.Usuario.nombre,
            func.count(modelos.Destino.id)
        ).join(modelos.Destino).group_by(modelos.Usuario.nombre).all()
    )
    
    # Destinos por mes
    destinos_por_mes = dict(
        db.query(
            func.date_trunc('month', modelos.Destino.fecha_destino).label('mes'),
            func.count(modelos.Destino.id)
        ).group_by('mes').all()
    )
    
    # Promedios
    destinos = db.query(modelos.Destino).all()
    promedio_cumplimiento = sum(d.cumplimiento_objetivos or 0 for d in destinos) / total_destinos if total_destinos > 0 else 0
    promedio_presupuesto = sum(d.presupuesto_final or 0 for d in destinos) / total_destinos if total_destinos > 0 else 0
    total_presupuesto = sum(d.presupuesto_final or 0 for d in destinos)
    
    # Estados
    destinos_pendientes = db.query(func.count(modelos.Destino.id)).filter(
        modelos.Destino.estado_id == 1
    ).scalar()
    
    destinos_completados = db.query(func.count(modelos.Destino.id)).filter(
        modelos.Destino.estado_id == 2
    ).scalar()
    
    destinos_en_proceso = db.query(func.count(modelos.Destino.id)).filter(
        modelos.Destino.estado_id == 3
    ).scalar()
    
    # Evaluaciones y lecciones
    evaluaciones = {}
    impactos = {}
    lecciones = []
    
    for destino in destinos:
        if destino.evaluacion:
            for key, value in destino.evaluacion.items():
                if key not in evaluaciones:
                    evaluaciones[key] = []
                evaluaciones[key].append(value)
        
        if destino.impacto:
            impactos[destino.impacto] = impactos.get(destino.impacto, 0) + 1
        
        if destino.lecciones_aprendidas:
            lecciones.append(destino.lecciones_aprendidas)
    
    # Calcular promedios de evaluaciones
    evaluaciones_promedio = {
        key: sum(values) / len(values)
        for key, values in evaluaciones.items()
    }
    
    return DestinoEstadisticas(
        total_destinos=total_destinos,
        destinos_por_tipo=destinos_por_tipo,
        destinos_por_estado=destinos_por_estado,
        destinos_por_responsable=destinos_por_responsable,
        destinos_por_mes=destinos_por_mes,
        promedio_cumplimiento=promedio_cumplimiento,
        promedio_presupuesto_final=promedio_presupuesto,
        total_presupuesto_final=total_presupuesto,
        destinos_pendientes=destinos_pendientes,
        destinos_completados=destinos_completados,
        destinos_en_proceso=destinos_en_proceso,
        evaluaciones_promedio=evaluaciones_promedio,
        impactos_mas_comunes=impactos,
        lecciones_aprendidas=lecciones
    )
