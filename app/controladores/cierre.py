from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, extract
from typing import List, Optional
from datetime import datetime, timedelta
import os
import json

from app import modelos
from app.db.session import get_db
from app.esquemas.cierre import (
    Cierre as CierreSchema,
    CierreCreate,
    CierreUpdate,
    CierreEstadisticas
)
from app.core.seguridad import get_current_user

router = APIRouter(
    prefix="/cierres",
    tags=["cierres"]
)

# Configurar directorio para documentos
UPLOAD_DIR = "uploads/cierres"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/", response_model=List[CierreSchema])
def read_cierres(
    skip: int = 0,
    limit: int = 100,
    tipo_cierre: Optional[str] = None,
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
            detail="No tiene permisos para ver los cierres"
        )
    
    query = db.query(modelos.Cierre)
    
    if tipo_cierre:
        query = query.filter(modelos.Cierre.tipo_cierre == tipo_cierre)
    if entidad_id:
        query = query.filter(modelos.Cierre.entidad_id == entidad_id)
    if responsable_id:
        query = query.filter(modelos.Cierre.responsable_id == responsable_id)
    if estado_id:
        query = query.filter(modelos.Cierre.estado_id == estado_id)
    if fecha_inicio and fecha_fin:
        query = query.filter(
            and_(
                modelos.Cierre.fecha_cierre >= fecha_inicio,
                modelos.Cierre.fecha_cierre <= fecha_fin
            )
        )
    if search:
        query = query.filter(
            or_(
                modelos.Cierre.nombre.ilike(f"%{search}%"),
                modelos.Cierre.descripcion.ilike(f"%{search}%"),
                modelos.Cierre.observaciones.ilike(f"%{search}%")
            )
        )
    
    cierres = query.order_by(modelos.Cierre.fecha_cierre.desc()).offset(skip).limit(limit).all()
    return cierres

@router.get("/{cierre_id}", response_model=CierreSchema)
def read_cierre(
    cierre_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre not in ["Admin", "Investigador"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para ver los cierres"
        )
    
    cierre = db.query(modelos.Cierre).filter(
        modelos.Cierre.id == cierre_id
    ).first()
    if cierre is None:
        raise HTTPException(status_code=404, detail="Cierre no encontrado")
    return cierre

@router.post("/", response_model=CierreSchema)
def create_cierre(
    cierre: CierreCreate,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre not in ["Admin", "Investigador"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para crear cierres"
        )
    
    # Verificar que la entidad existe
    if cierre.tipo_cierre == "proyecto":
        entidad = db.query(modelos.Proyecto).filter(
            modelos.Proyecto.id == cierre.entidad_id
        ).first()
    else:  # convocatoria
        entidad = db.query(modelos.Convocatoria).filter(
            modelos.Convocatoria.id == cierre.entidad_id
        ).first()
    
    if not entidad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La {cierre.tipo_cierre} especificada no existe"
        )
    
    # Verificar que no existe un cierre previo
    cierre_existente = db.query(modelos.Cierre).filter(
        and_(
            modelos.Cierre.tipo_cierre == cierre.tipo_cierre,
            modelos.Cierre.entidad_id == cierre.entidad_id
        )
    ).first()
    
    if cierre_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un cierre para esta {cierre.tipo_cierre}"
        )
    
    db_cierre = modelos.Cierre(**cierre.dict())
    db.add(db_cierre)
    db.commit()
    db.refresh(db_cierre)
    return db_cierre

@router.put("/{cierre_id}", response_model=CierreSchema)
def update_cierre(
    cierre_id: int,
    cierre: CierreUpdate,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre not in ["Admin", "Investigador"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para actualizar cierres"
        )
    
    db_cierre = db.query(modelos.Cierre).filter(
        modelos.Cierre.id == cierre_id
    ).first()
    if db_cierre is None:
        raise HTTPException(status_code=404, detail="Cierre no encontrado")
    
    # Verificar permisos específicos
    if current_user.rol.nombre != "Admin" and db_cierre.responsable_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo puede actualizar sus propios cierres"
        )
    
    # Actualizar campos
    for key, value in cierre.dict(exclude_unset=True).items():
        setattr(db_cierre, key, value)
    
    db_cierre.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_cierre)
    return db_cierre

@router.delete("/{cierre_id}", response_model=CierreSchema)
def delete_cierre(
    cierre_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden eliminar cierres"
        )
    
    db_cierre = db.query(modelos.Cierre).filter(
        modelos.Cierre.id == cierre_id
    ).first()
    if db_cierre is None:
        raise HTTPException(status_code=404, detail="Cierre no encontrado")
    
    # Eliminar documentos asociados
    if db_cierre.documentos:
        for doc in db_cierre.documentos:
            try:
                os.remove(os.path.join(UPLOAD_DIR, doc))
            except:
                pass
    
    db.delete(db_cierre)
    db.commit()
    return db_cierre

@router.post("/{cierre_id}/documentos")
async def upload_documento(
    cierre_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre not in ["Admin", "Investigador"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para subir documentos"
        )
    
    db_cierre = db.query(modelos.Cierre).filter(
        modelos.Cierre.id == cierre_id
    ).first()
    if db_cierre is None:
        raise HTTPException(status_code=404, detail="Cierre no encontrado")
    
    # Generar nombre único para el archivo
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"{cierre_id}_{timestamp}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    # Guardar archivo
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Actualizar lista de documentos
    documentos = db_cierre.documentos or []
    documentos.append(filename)
    db_cierre.documentos = documentos
    db_cierre.fecha_actualizacion = datetime.utcnow()
    
    db.commit()
    db.refresh(db_cierre)
    return {"filename": filename}

@router.get("/estadisticas/", response_model=CierreEstadisticas)
def get_estadisticas_cierres(
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden ver las estadísticas"
        )
    
    # Total de cierres
    total_cierres = db.query(func.count(modelos.Cierre.id)).scalar()
    
    # Cierres por tipo
    cierres_por_tipo = dict(
        db.query(
            modelos.Cierre.tipo_cierre,
            func.count(modelos.Cierre.id)
        ).group_by(modelos.Cierre.tipo_cierre).all()
    )
    
    # Cierres por estado
    cierres_por_estado = dict(
        db.query(
            modelos.Estado.nombre,
            func.count(modelos.Cierre.id)
        ).join(modelos.Cierre).group_by(modelos.Estado.nombre).all()
    )
    
    # Cierres por responsable
    cierres_por_responsable = dict(
        db.query(
            modelos.Usuario.nombre,
            func.count(modelos.Cierre.id)
        ).join(modelos.Cierre).group_by(modelos.Usuario.nombre).all()
    )
    
    # Cierres por mes
    cierres_por_mes = dict(
        db.query(
            func.date_trunc('month', modelos.Cierre.fecha_cierre).label('mes'),
            func.count(modelos.Cierre.id)
        ).group_by('mes').all()
    )
    
    # Promedios
    cierres = db.query(modelos.Cierre).all()
    promedio_cumplimiento = sum(c.cumplimiento_objetivos or 0 for c in cierres) / total_cierres if total_cierres > 0 else 0
    promedio_presupuesto = sum(c.presupuesto_final or 0 for c in cierres) / total_cierres if total_cierres > 0 else 0
    total_presupuesto = sum(c.presupuesto_final or 0 for c in cierres)
    
    # Estados
    cierres_pendientes = db.query(func.count(modelos.Cierre.id)).filter(
        modelos.Cierre.estado_id == 1
    ).scalar()
    
    cierres_completados = db.query(func.count(modelos.Cierre.id)).filter(
        modelos.Cierre.estado_id == 2
    ).scalar()
    
    cierres_en_proceso = db.query(func.count(modelos.Cierre.id)).filter(
        modelos.Cierre.estado_id == 3
    ).scalar()
    
    # Evaluaciones y lecciones
    evaluaciones = {}
    impactos = {}
    lecciones = []
    
    for cierre in cierres:
        if cierre.evaluacion:
            for key, value in cierre.evaluacion.items():
                if key not in evaluaciones:
                    evaluaciones[key] = []
                evaluaciones[key].append(value)
        
        if cierre.impacto:
            impactos[cierre.impacto] = impactos.get(cierre.impacto, 0) + 1
        
        if cierre.lecciones_aprendidas:
            lecciones.append(cierre.lecciones_aprendidas)
    
    # Calcular promedios de evaluaciones
    evaluaciones_promedio = {
        key: sum(values) / len(values)
        for key, values in evaluaciones.items()
    }
    
    return CierreEstadisticas(
        total_cierres=total_cierres,
        cierres_por_tipo=cierres_por_tipo,
        cierres_por_estado=cierres_por_estado,
        cierres_por_responsable=cierres_por_responsable,
        cierres_por_mes=cierres_por_mes,
        promedio_cumplimiento=promedio_cumplimiento,
        promedio_presupuesto_final=promedio_presupuesto,
        total_presupuesto_final=total_presupuesto,
        cierres_pendientes=cierres_pendientes,
        cierres_completados=cierres_completados,
        cierres_en_proceso=cierres_en_proceso,
        evaluaciones_promedio=evaluaciones_promedio,
        impactos_mas_comunes=impactos,
        lecciones_aprendidas=lecciones
    )
