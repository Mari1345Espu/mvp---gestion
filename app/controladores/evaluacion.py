from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, extract
from typing import List, Optional
from datetime import datetime
import os
import shutil

from app import modelos
from app.db.session import get_db
from app.esquemas.evaluacion import (
    Evaluacion as EvaluacionSchema,
    EvaluacionCreate,
    EvaluacionUpdate,
    EvaluacionEstadisticas
)
from app.core.seguridad import get_current_user

router = APIRouter(
    prefix="/evaluaciones",
    tags=["evaluaciones"]
)

# Configuración del directorio de uploads
UPLOAD_DIR = "uploads/evaluaciones"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Roles permitidos para gestionar evaluaciones
ROLES_PERMITIDOS = ["Admin", "Evaluador", "Asesor"]

@router.get("/", response_model=List[EvaluacionSchema])
def read_evaluaciones(
    skip: int = 0,
    limit: int = 100,
    tipo_evaluacion: Optional[str] = None,
    entidad_id: Optional[int] = None,
    responsable_id: Optional[int] = None,
    estado_id: Optional[int] = None,
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre not in ROLES_PERMITIDOS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver las evaluaciones"
        )
    
    query = db.query(modelos.Evaluacion)
    
    # Si no es admin, solo puede ver sus propias evaluaciones
    if current_user.rol.nombre != "Admin":
        query = query.filter(modelos.Evaluacion.responsable_id == current_user.id)
    
    if tipo_evaluacion:
        query = query.filter(modelos.Evaluacion.tipo_evaluacion == tipo_evaluacion)
    if entidad_id:
        query = query.filter(modelos.Evaluacion.entidad_id == entidad_id)
    if responsable_id:
        query = query.filter(modelos.Evaluacion.responsable_id == responsable_id)
    if estado_id:
        query = query.filter(modelos.Evaluacion.estado_id == estado_id)
    if fecha_inicio:
        query = query.filter(modelos.Evaluacion.fecha_evaluacion >= fecha_inicio)
    if fecha_fin:
        query = query.filter(modelos.Evaluacion.fecha_evaluacion <= fecha_fin)
    if search:
        query = query.filter(
            or_(
                modelos.Evaluacion.nombre.ilike(f"%{search}%"),
                modelos.Evaluacion.descripcion.ilike(f"%{search}%"),
                modelos.Evaluacion.observaciones.ilike(f"%{search}%")
            )
        )
    
    evaluaciones = query.order_by(modelos.Evaluacion.fecha_evaluacion.desc()).offset(skip).limit(limit).all()
    return evaluaciones

@router.get("/{evaluacion_id}", response_model=EvaluacionSchema)
def read_evaluacion(
    evaluacion_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre not in ROLES_PERMITIDOS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver las evaluaciones"
        )
    
    evaluacion = db.query(modelos.Evaluacion).filter(
        modelos.Evaluacion.id == evaluacion_id
    ).first()
    if evaluacion is None:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    
    # Si no es admin, solo puede ver sus propias evaluaciones
    if current_user.rol.nombre != "Admin" and evaluacion.responsable_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para ver esta evaluación"
        )
    
    return evaluacion

@router.post("/", response_model=EvaluacionSchema)
def create_evaluacion(
    evaluacion: EvaluacionCreate,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre not in ROLES_PERMITIDOS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para crear evaluaciones"
        )
    
    # Si no es admin, solo puede crear evaluaciones asignadas a sí mismo
    if current_user.rol.nombre != "Admin" and evaluacion.responsable_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo puedes crear evaluaciones asignadas a ti mismo"
        )
    
    # Verificar que la entidad existe
    entidad = db.query(modelos.Proyecto).filter(
        modelos.Proyecto.id == evaluacion.entidad_id
    ).first()
    if not entidad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La entidad especificada no existe"
        )
    
    # Verificar que el responsable existe
    responsable = db.query(modelos.Usuario).filter(
        modelos.Usuario.id == evaluacion.responsable_id
    ).first()
    if not responsable:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El responsable especificado no existe"
        )
    
    # Verificar que el estado existe
    estado = db.query(modelos.Estado).filter(
        modelos.Estado.id == evaluacion.estado_id
    ).first()
    if not estado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El estado especificado no existe"
        )
    
    db_evaluacion = modelos.Evaluacion(**evaluacion.dict())
    db.add(db_evaluacion)
    db.commit()
    db.refresh(db_evaluacion)
    return db_evaluacion

@router.put("/{evaluacion_id}", response_model=EvaluacionSchema)
def update_evaluacion(
    evaluacion_id: int,
    evaluacion: EvaluacionUpdate,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre not in ROLES_PERMITIDOS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para actualizar evaluaciones"
        )
    
    db_evaluacion = db.query(modelos.Evaluacion).filter(
        modelos.Evaluacion.id == evaluacion_id
    ).first()
    if db_evaluacion is None:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    
    # Si no es admin, solo puede actualizar sus propias evaluaciones
    if current_user.rol.nombre != "Admin" and db_evaluacion.responsable_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para actualizar esta evaluación"
        )
    
    # Si no es admin, no puede cambiar el responsable
    if current_user.rol.nombre != "Admin" and evaluacion.responsable_id and evaluacion.responsable_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No puedes cambiar el responsable de la evaluación"
        )
    
    # Verificar que el responsable existe si se está actualizando
    if evaluacion.responsable_id:
        responsable = db.query(modelos.Usuario).filter(
            modelos.Usuario.id == evaluacion.responsable_id
        ).first()
        if not responsable:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El responsable especificado no existe"
            )
    
    # Verificar que el estado existe si se está actualizando
    if evaluacion.estado_id:
        estado = db.query(modelos.Estado).filter(
            modelos.Estado.id == evaluacion.estado_id
        ).first()
        if not estado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El estado especificado no existe"
            )
    
    # Actualizar campos
    for key, value in evaluacion.dict(exclude_unset=True).items():
        setattr(db_evaluacion, key, value)
    
    db_evaluacion.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_evaluacion)
    return db_evaluacion

@router.delete("/{evaluacion_id}", response_model=EvaluacionSchema)
def delete_evaluacion(
    evaluacion_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden eliminar evaluaciones"
        )
    
    db_evaluacion = db.query(modelos.Evaluacion).filter(
        modelos.Evaluacion.id == evaluacion_id
    ).first()
    if db_evaluacion is None:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    
    # Eliminar documentos asociados
    if db_evaluacion.documentos:
        for doc in db_evaluacion.documentos:
            try:
                os.remove(os.path.join(UPLOAD_DIR, doc))
            except:
                pass
    
    db.delete(db_evaluacion)
    db.commit()
    return db_evaluacion

@router.post("/{evaluacion_id}/documentos", response_model=EvaluacionSchema)
async def upload_documentos(
    evaluacion_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre not in ROLES_PERMITIDOS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para subir documentos"
        )
    
    db_evaluacion = db.query(modelos.Evaluacion).filter(
        modelos.Evaluacion.id == evaluacion_id
    ).first()
    if db_evaluacion is None:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    
    # Si no es admin, solo puede subir documentos a sus propias evaluaciones
    if current_user.rol.nombre != "Admin" and db_evaluacion.responsable_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para subir documentos a esta evaluación"
        )
    
    documentos = db_evaluacion.documentos or []
    
    for file in files:
        # Generar nombre único para el archivo
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{evaluacion_id}_{timestamp}_{file.filename}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        
        # Guardar archivo
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        documentos.append(filename)
    
    db_evaluacion.documentos = documentos
    db_evaluacion.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_evaluacion)
    return db_evaluacion

@router.get("/estadisticas/", response_model=EvaluacionEstadisticas)
def get_estadisticas_evaluaciones(
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden ver las estadísticas"
        )
    
    # Total de evaluaciones
    total_evaluaciones = db.query(func.count(modelos.Evaluacion.id)).scalar()
    
    # Evaluaciones por tipo
    evaluaciones_por_tipo = dict(
        db.query(
            modelos.Evaluacion.tipo_evaluacion,
            func.count(modelos.Evaluacion.id)
        ).group_by(modelos.Evaluacion.tipo_evaluacion).all()
    )
    
    # Evaluaciones por estado
    evaluaciones_por_estado = dict(
        db.query(
            modelos.Estado.nombre,
            func.count(modelos.Evaluacion.id)
        ).join(modelos.Evaluacion).group_by(modelos.Estado.nombre).all()
    )
    
    # Evaluaciones por responsable
    evaluaciones_por_responsable = dict(
        db.query(
            modelos.Usuario.nombre,
            func.count(modelos.Evaluacion.id)
        ).join(modelos.Evaluacion).group_by(modelos.Usuario.nombre).all()
    )
    
    # Evaluaciones por mes
    evaluaciones_por_mes = dict(
        db.query(
            extract('month', modelos.Evaluacion.fecha_evaluacion),
            func.count(modelos.Evaluacion.id)
        ).group_by(extract('month', modelos.Evaluacion.fecha_evaluacion)).all()
    )
    
    # Evaluaciones por día
    evaluaciones_por_dia = dict(
        db.query(
            extract('day', modelos.Evaluacion.fecha_evaluacion),
            func.count(modelos.Evaluacion.id)
        ).group_by(extract('day', modelos.Evaluacion.fecha_evaluacion)).all()
    )
    
    # Evaluaciones por hora
    evaluaciones_por_hora = dict(
        db.query(
            extract('hour', modelos.Evaluacion.fecha_evaluacion),
            func.count(modelos.Evaluacion.id)
        ).group_by(extract('hour', modelos.Evaluacion.fecha_evaluacion)).all()
    )
    
    # Promedios
    promedio_puntuacion = db.query(func.avg(modelos.Evaluacion.puntuacion)).scalar() or 0
    promedio_cumplimiento = db.query(func.avg(modelos.Evaluacion.cumplimiento_objetivos)).scalar() or 0
    promedio_presupuesto = db.query(func.avg(modelos.Evaluacion.presupuesto_final)).scalar() or 0
    
    # Totales
    total_documentos = db.query(func.count(modelos.Evaluacion.documentos)).scalar() or 0
    total_recomendaciones = db.query(func.count(modelos.Evaluacion.recomendaciones)).scalar() or 0
    total_lecciones = db.query(func.count(modelos.Evaluacion.lecciones_aprendidas)).scalar() or 0
    
    return EvaluacionEstadisticas(
        total_evaluaciones=total_evaluaciones,
        evaluaciones_por_tipo=evaluaciones_por_tipo,
        evaluaciones_por_estado=evaluaciones_por_estado,
        evaluaciones_por_responsable=evaluaciones_por_responsable,
        evaluaciones_por_mes=evaluaciones_por_mes,
        evaluaciones_por_dia=evaluaciones_por_dia,
        evaluaciones_por_hora=evaluaciones_por_hora,
        promedio_puntuacion=promedio_puntuacion,
        promedio_cumplimiento=promedio_cumplimiento,
        promedio_presupuesto=promedio_presupuesto,
        total_documentos=total_documentos,
        total_recomendaciones=total_recomendaciones,
        total_lecciones=total_lecciones
    )
