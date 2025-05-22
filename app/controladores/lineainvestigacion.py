from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional
from datetime import datetime

from app import modelos
from app.db.session import get_db
from app.esquemas.lineainvestigacion import (
    LineaInvestigacion as LineaInvestigacionSchema,
    LineaInvestigacionCreate,
    LineaInvestigacionUpdate,
    LineaInvestigacionEstadisticas
)
from app.core.seguridad import get_current_user

router = APIRouter(
    prefix="/lineas-investigacion",
    tags=["lineas-investigacion"]
)

@router.get("/", response_model=List[LineaInvestigacionSchema])
def read_lineas(
    skip: int = 0,
    limit: int = 100,
    grupo_id: Optional[int] = None,
    estado_id: Optional[int] = None,
    coordinador_id: Optional[int] = None,
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    query = db.query(modelos.LineaInvestigacion)
    
    if grupo_id:
        query = query.filter(modelos.LineaInvestigacion.grupo_investigacion_id == grupo_id)
    if estado_id:
        query = query.filter(modelos.LineaInvestigacion.estado_id == estado_id)
    if coordinador_id:
        query = query.filter(modelos.LineaInvestigacion.coordinador_id == coordinador_id)
    if fecha_inicio and fecha_fin:
        query = query.filter(
            and_(
                modelos.LineaInvestigacion.fecha_creacion >= fecha_inicio,
                modelos.LineaInvestigacion.fecha_creacion <= fecha_fin
            )
        )
    if search:
        query = query.filter(
            or_(
                modelos.LineaInvestigacion.nombre.ilike(f"%{search}%"),
                modelos.LineaInvestigacion.descripcion.ilike(f"%{search}%"),
                modelos.LineaInvestigacion.objetivos.ilike(f"%{search}%")
            )
        )
    
    lineas = query.offset(skip).limit(limit).all()
    return lineas

@router.get("/{linea_id}", response_model=LineaInvestigacionSchema)
def read_linea(
    linea_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    linea = db.query(modelos.LineaInvestigacion).filter(modelos.LineaInvestigacion.id == linea_id).first()
    if linea is None:
        raise HTTPException(status_code=404, detail="Línea de investigación no encontrada")
    return linea

@router.post("/", response_model=LineaInvestigacionSchema)
def create_linea(
    linea: LineaInvestigacionCreate,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre not in ["Admin", "Investigador"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para crear líneas de investigación"
        )
    
    # Verificar que el grupo existe
    grupo = db.query(modelos.GrupoInvestigacion).filter(
        modelos.GrupoInvestigacion.id == linea.grupo_investigacion_id
    ).first()
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo de investigación no encontrado")
    
    # Verificar que el coordinador existe si se proporciona
    if linea.coordinador_id:
        coordinador = db.query(modelos.Usuario).filter(modelos.Usuario.id == linea.coordinador_id).first()
        if not coordinador:
            raise HTTPException(status_code=404, detail="Coordinador no encontrado")
    
    db_linea = modelos.LineaInvestigacion(**linea.dict())
    db.add(db_linea)
    db.commit()
    db.refresh(db_linea)
    return db_linea

@router.put("/{linea_id}", response_model=LineaInvestigacionSchema)
def update_linea(
    linea_id: int,
    linea: LineaInvestigacionUpdate,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre not in ["Admin", "Investigador"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para actualizar líneas de investigación"
        )
    
    db_linea = db.query(modelos.LineaInvestigacion).filter(modelos.LineaInvestigacion.id == linea_id).first()
    if db_linea is None:
        raise HTTPException(status_code=404, detail="Línea de investigación no encontrada")
    
    # Verificar que el coordinador existe si se proporciona
    if linea.coordinador_id:
        coordinador = db.query(modelos.Usuario).filter(modelos.Usuario.id == linea.coordinador_id).first()
        if not coordinador:
            raise HTTPException(status_code=404, detail="Coordinador no encontrado")
    
    # Actualizar campos
    for key, value in linea.dict(exclude_unset=True).items():
        setattr(db_linea, key, value)
    
    db_linea.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_linea)
    return db_linea

@router.delete("/{linea_id}", response_model=LineaInvestigacionSchema)
def delete_linea(
    linea_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden eliminar líneas de investigación"
        )
    
    db_linea = db.query(modelos.LineaInvestigacion).filter(modelos.LineaInvestigacion.id == linea_id).first()
    if db_linea is None:
        raise HTTPException(status_code=404, detail="Línea de investigación no encontrada")
    
    db.delete(db_linea)
    db.commit()
    return db_linea

@router.get("/estadisticas/", response_model=LineaInvestigacionEstadisticas)
def get_estadisticas_lineas(
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden ver las estadísticas"
        )
    
    # Total de líneas
    total_lineas = db.query(func.count(modelos.LineaInvestigacion.id)).scalar()
    
    # Líneas por estado
    lineas_por_estado = dict(
        db.query(
            modelos.Estado.nombre,
            func.count(modelos.LineaInvestigacion.id)
        ).join(modelos.LineaInvestigacion).group_by(modelos.Estado.nombre).all()
    )
    
    # Líneas por tipo de estado
    lineas_por_tipo_estado = dict(
        db.query(
            modelos.TipoEstado.nombre,
            func.count(modelos.LineaInvestigacion.id)
        ).join(modelos.LineaInvestigacion).group_by(modelos.TipoEstado.nombre).all()
    )
    
    # Líneas por grupo
    lineas_por_grupo = dict(
        db.query(
            modelos.GrupoInvestigacion.nombre,
            func.count(modelos.LineaInvestigacion.id)
        ).join(modelos.LineaInvestigacion).group_by(modelos.GrupoInvestigacion.nombre).all()
    )
    
    # Líneas activas e inactivas
    lineas_activas = db.query(func.count(modelos.LineaInvestigacion.id)).filter(
        modelos.LineaInvestigacion.estado_id == 1  # Asumiendo que 1 es el ID del estado "Activo"
    ).scalar()
    
    lineas_inactivas = db.query(func.count(modelos.LineaInvestigacion.id)).filter(
        modelos.LineaInvestigacion.estado_id == 2  # Asumiendo que 2 es el ID del estado "Inactivo"
    ).scalar()
    
    # Líneas por mes
    lineas_por_mes = dict(
        db.query(
            func.date_trunc('month', modelos.LineaInvestigacion.fecha_creacion).label('mes'),
            func.count(modelos.LineaInvestigacion.id)
        ).group_by('mes').all()
    )
    
    # Promedios y conteos
    lineas = db.query(modelos.LineaInvestigacion).all()
    total_proyectos = 0
    total_productos = 0
    total_investigadores = 0
    lineas_por_coordinador = {}
    
    for linea in lineas:
        # Contar proyectos
        proyectos = db.query(func.count(modelos.Proyecto.id)).filter(
            modelos.Proyecto.linea_investigacion_id == linea.id
        ).scalar()
        total_proyectos += proyectos
        
        # Contar productos
        productos = db.query(func.count(modelos.Producto.id)).join(
            modelos.Proyecto
        ).filter(
            modelos.Proyecto.linea_investigacion_id == linea.id
        ).scalar()
        total_productos += productos
        
        # Contar investigadores
        investigadores = db.query(func.count(modelos.Usuario.id)).filter(
            modelos.Usuario.linea_investigacion_id == linea.id
        ).scalar()
        total_investigadores += investigadores
        
        # Agrupar por coordinador
        if linea.coordinador_id:
            coordinador = db.query(modelos.Usuario).filter(modelos.Usuario.id == linea.coordinador_id).first()
            if coordinador:
                coordinador_nombre = coordinador.nombre
                lineas_por_coordinador[coordinador_nombre] = lineas_por_coordinador.get(coordinador_nombre, 0) + 1
    
    promedio_proyectos = total_proyectos / total_lineas if total_lineas > 0 else 0
    promedio_productos = total_productos / total_lineas if total_lineas > 0 else 0
    promedio_investigadores = total_investigadores / total_lineas if total_lineas > 0 else 0
    
    return LineaInvestigacionEstadisticas(
        total_lineas=total_lineas,
        lineas_por_estado=lineas_por_estado,
        lineas_por_tipo_estado=lineas_por_tipo_estado,
        lineas_por_grupo=lineas_por_grupo,
        lineas_activas=lineas_activas,
        lineas_inactivas=lineas_inactivas,
        lineas_por_mes=lineas_por_mes,
        promedio_proyectos=promedio_proyectos,
        promedio_productos=promedio_productos,
        promedio_investigadores=promedio_investigadores,
        lineas_por_coordinador=lineas_por_coordinador
    )

@router.put("/{linea_id}/asignar-coordinador", response_model=LineaInvestigacionSchema)
def asignar_coordinador(
    linea_id: int,
    coordinador_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden asignar coordinadores"
        )
    
    db_linea = db.query(modelos.LineaInvestigacion).filter(modelos.LineaInvestigacion.id == linea_id).first()
    if db_linea is None:
        raise HTTPException(status_code=404, detail="Línea de investigación no encontrada")
    
    coordinador = db.query(modelos.Usuario).filter(modelos.Usuario.id == coordinador_id).first()
    if not coordinador:
        raise HTTPException(status_code=404, detail="Coordinador no encontrado")
    
    db_linea.coordinador_id = coordinador_id
    db_linea.fecha_actualizacion = datetime.utcnow()
    
    db.commit()
    db.refresh(db_linea)
    return db_linea
