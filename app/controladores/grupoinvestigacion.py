from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional
from datetime import datetime, timedelta
import os

from app import modelos
from app.db.session import get_db
from app.esquemas.grupoinvestigacion import (
    GrupoInvestigacion as GrupoInvestigacionSchema,
    GrupoInvestigacionCreate,
    GrupoInvestigacionUpdate,
    GrupoInvestigacionEstadisticas
)
from app.core.seguridad import get_current_user

router = APIRouter(
    prefix="/grupos-investigacion",
    tags=["grupos-investigacion"]
)

@router.get("/", response_model=List[GrupoInvestigacionSchema])
def read_grupos(
    skip: int = 0,
    limit: int = 100,
    estado_id: Optional[int] = None,
    director_id: Optional[int] = None,
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    query = db.query(modelos.GrupoInvestigacion)
    
    if estado_id:
        query = query.filter(modelos.GrupoInvestigacion.estado_id == estado_id)
    if director_id:
        query = query.filter(modelos.GrupoInvestigacion.director_id == director_id)
    if fecha_inicio and fecha_fin:
        query = query.filter(
            and_(
                modelos.GrupoInvestigacion.fecha_creacion >= fecha_inicio,
                modelos.GrupoInvestigacion.fecha_creacion <= fecha_fin
            )
        )
    if search:
        query = query.filter(
            or_(
                modelos.GrupoInvestigacion.nombre.ilike(f"%{search}%"),
                modelos.GrupoInvestigacion.codigo.ilike(f"%{search}%"),
                modelos.GrupoInvestigacion.descripcion.ilike(f"%{search}%")
            )
        )
    
    grupos = query.offset(skip).limit(limit).all()
    return grupos

@router.get("/{grupo_id}", response_model=GrupoInvestigacionSchema)
def read_grupo(
    grupo_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    grupo = db.query(modelos.GrupoInvestigacion).filter(modelos.GrupoInvestigacion.id == grupo_id).first()
    if grupo is None:
        raise HTTPException(status_code=404, detail="Grupo de investigación no encontrado")
    return grupo

@router.post("/", response_model=GrupoInvestigacionSchema)
async def create_grupo(
    nombre: str = Form(...),
    codigo: str = Form(...),
    descripcion: str = Form(...),
    fecha_creacion: datetime = Form(...),
    director_id: int = Form(...),
    estado_id: int = Form(...),
    tipo_estado_id: int = Form(...),
    logo: UploadFile = File(None),
    fecha_renovacion: Optional[datetime] = Form(None),
    fecha_vencimiento: Optional[datetime] = Form(None),
    correo: Optional[str] = Form(None),
    telefono: Optional[str] = Form(None),
    pagina_web: Optional[str] = Form(None),
    lineas_investigacion: Optional[str] = Form(None),
    observaciones: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden crear grupos de investigación"
        )
    
    # Verificar que el director existe
    director = db.query(modelos.Usuario).filter(modelos.Usuario.id == director_id).first()
    if not director:
        raise HTTPException(status_code=404, detail="Director no encontrado")
    
    # Manejar el logo si se proporciona
    logo_url = None
    if logo:
        uploads_dir = os.path.join("app", "static", "uploads", "grupos")
        os.makedirs(uploads_dir, exist_ok=True)
        file_ext = os.path.splitext(logo.filename)[1]
        file_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{logo.filename}"
        file_path = os.path.join(uploads_dir, file_name)
        with open(file_path, "wb") as f:
            f.write(await logo.read())
        logo_url = f"/static/uploads/grupos/{file_name}"
    
    db_grupo = modelos.GrupoInvestigacion(
        nombre=nombre,
        codigo=codigo,
        descripcion=descripcion,
        fecha_creacion=fecha_creacion,
        director_id=director_id,
        estado_id=estado_id,
        tipo_estado_id=tipo_estado_id,
        fecha_renovacion=fecha_renovacion,
        fecha_vencimiento=fecha_vencimiento,
        correo=correo,
        telefono=telefono,
        pagina_web=pagina_web,
        logo=logo_url,
        lineas_investigacion=lineas_investigacion,
        observaciones=observaciones
    )
    
    db.add(db_grupo)
    db.commit()
    db.refresh(db_grupo)
    return db_grupo

@router.put("/{grupo_id}", response_model=GrupoInvestigacionSchema)
async def update_grupo(
    grupo_id: int,
    nombre: Optional[str] = Form(None),
    codigo: Optional[str] = Form(None),
    descripcion: Optional[str] = Form(None),
    director_id: Optional[int] = Form(None),
    estado_id: Optional[int] = Form(None),
    tipo_estado_id: Optional[int] = Form(None),
    logo: Optional[UploadFile] = File(None),
    fecha_renovacion: Optional[datetime] = Form(None),
    fecha_vencimiento: Optional[datetime] = Form(None),
    correo: Optional[str] = Form(None),
    telefono: Optional[str] = Form(None),
    pagina_web: Optional[str] = Form(None),
    lineas_investigacion: Optional[str] = Form(None),
    observaciones: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden actualizar grupos de investigación"
        )
    
    db_grupo = db.query(modelos.GrupoInvestigacion).filter(modelos.GrupoInvestigacion.id == grupo_id).first()
    if db_grupo is None:
        raise HTTPException(status_code=404, detail="Grupo de investigación no encontrado")
    
    # Verificar que el director existe si se proporciona
    if director_id:
        director = db.query(modelos.Usuario).filter(modelos.Usuario.id == director_id).first()
        if not director:
            raise HTTPException(status_code=404, detail="Director no encontrado")
    
    # Manejar el logo si se proporciona
    if logo:
        uploads_dir = os.path.join("app", "static", "uploads", "grupos")
        os.makedirs(uploads_dir, exist_ok=True)
        file_ext = os.path.splitext(logo.filename)[1]
        file_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{logo.filename}"
        file_path = os.path.join(uploads_dir, file_name)
        with open(file_path, "wb") as f:
            f.write(await logo.read())
        db_grupo.logo = f"/static/uploads/grupos/{file_name}"
    
    # Actualizar campos
    if nombre is not None:
        db_grupo.nombre = nombre
    if codigo is not None:
        db_grupo.codigo = codigo
    if descripcion is not None:
        db_grupo.descripcion = descripcion
    if director_id is not None:
        db_grupo.director_id = director_id
    if estado_id is not None:
        db_grupo.estado_id = estado_id
    if tipo_estado_id is not None:
        db_grupo.tipo_estado_id = tipo_estado_id
    if fecha_renovacion is not None:
        db_grupo.fecha_renovacion = fecha_renovacion
    if fecha_vencimiento is not None:
        db_grupo.fecha_vencimiento = fecha_vencimiento
    if correo is not None:
        db_grupo.correo = correo
    if telefono is not None:
        db_grupo.telefono = telefono
    if pagina_web is not None:
        db_grupo.pagina_web = pagina_web
    if lineas_investigacion is not None:
        db_grupo.lineas_investigacion = lineas_investigacion
    if observaciones is not None:
        db_grupo.observaciones = observaciones
    
    db_grupo.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_grupo)
    return db_grupo

@router.delete("/{grupo_id}", response_model=GrupoInvestigacionSchema)
def delete_grupo(
    grupo_id: int,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden eliminar grupos de investigación"
        )
    
    db_grupo = db.query(modelos.GrupoInvestigacion).filter(modelos.GrupoInvestigacion.id == grupo_id).first()
    if db_grupo is None:
        raise HTTPException(status_code=404, detail="Grupo de investigación no encontrado")
    
    # Eliminar logo si existe
    if db_grupo.logo:
        try:
            os.remove(os.path.join("app", db_grupo.logo.lstrip("/")))
        except:
            pass
    
    db.delete(db_grupo)
    db.commit()
    return db_grupo

@router.get("/estadisticas/", response_model=GrupoInvestigacionEstadisticas)
def get_estadisticas_grupos(
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden ver las estadísticas"
        )
    
    # Total de grupos
    total_grupos = db.query(func.count(modelos.GrupoInvestigacion.id)).scalar()
    
    # Grupos por estado
    grupos_por_estado = dict(
        db.query(
            modelos.Estado.nombre,
            func.count(modelos.GrupoInvestigacion.id)
        ).join(modelos.GrupoInvestigacion).group_by(modelos.Estado.nombre).all()
    )
    
    # Grupos por tipo de estado
    grupos_por_tipo_estado = dict(
        db.query(
            modelos.TipoEstado.nombre,
            func.count(modelos.GrupoInvestigacion.id)
        ).join(modelos.GrupoInvestigacion).group_by(modelos.TipoEstado.nombre).all()
    )
    
    # Grupos activos y vencidos
    grupos_activos = db.query(func.count(modelos.GrupoInvestigacion.id)).filter(
        and_(
            modelos.GrupoInvestigacion.estado_id == 1,  # Asumiendo que 1 es el ID del estado "Activo"
            or_(
                modelos.GrupoInvestigacion.fecha_vencimiento.is_(None),
                modelos.GrupoInvestigacion.fecha_vencimiento > datetime.utcnow()
            )
        )
    ).scalar()
    
    grupos_vencidos = db.query(func.count(modelos.GrupoInvestigacion.id)).filter(
        and_(
            modelos.GrupoInvestigacion.fecha_vencimiento.isnot(None),
            modelos.GrupoInvestigacion.fecha_vencimiento <= datetime.utcnow()
        )
    ).scalar()
    
    # Grupos por mes
    grupos_por_mes = dict(
        db.query(
            func.date_trunc('month', modelos.GrupoInvestigacion.fecha_creacion).label('mes'),
            func.count(modelos.GrupoInvestigacion.id)
        ).group_by('mes').all()
    )
    
    # Promedio de integrantes por grupo
    grupos = db.query(modelos.GrupoInvestigacion).all()
    total_integrantes = 0
    total_proyectos = 0
    total_productos = 0
    grupos_por_director = {}
    
    for grupo in grupos:
        # Contar integrantes
        integrantes = db.query(func.count(modelos.Usuario.id)).filter(
            modelos.Usuario.grupo_investigacion_id == grupo.id
        ).scalar()
        total_integrantes += integrantes
        
        # Contar proyectos
        proyectos = db.query(func.count(modelos.Proyecto.id)).filter(
            modelos.Proyecto.grupo_investigacion_id == grupo.id
        ).scalar()
        total_proyectos += proyectos
        
        # Contar productos
        productos = db.query(func.count(modelos.Producto.id)).join(
            modelos.Proyecto
        ).filter(
            modelos.Proyecto.grupo_investigacion_id == grupo.id
        ).scalar()
        total_productos += productos
        
        # Agrupar por director
        director = db.query(modelos.Usuario).filter(modelos.Usuario.id == grupo.director_id).first()
        if director:
            director_nombre = director.nombre
            grupos_por_director[director_nombre] = grupos_por_director.get(director_nombre, 0) + 1
    
    promedio_integrantes = total_integrantes / total_grupos if total_grupos > 0 else 0
    promedio_proyectos = total_proyectos / total_grupos if total_grupos > 0 else 0
    promedio_productos = total_productos / total_grupos if total_grupos > 0 else 0
    
    return GrupoInvestigacionEstadisticas(
        total_grupos=total_grupos,
        grupos_por_estado=grupos_por_estado,
        grupos_por_tipo_estado=grupos_por_tipo_estado,
        grupos_activos=grupos_activos,
        grupos_vencidos=grupos_vencidos,
        grupos_por_mes=grupos_por_mes,
        promedio_integrantes=promedio_integrantes,
        promedio_proyectos=promedio_proyectos,
        promedio_productos=promedio_productos,
        grupos_por_director=grupos_por_director
    )

@router.put("/{grupo_id}/renovar", response_model=GrupoInvestigacionSchema)
def renovar_grupo(
    grupo_id: int,
    fecha_vencimiento: datetime,
    observaciones: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: modelos.Usuario = Depends(get_current_user)
):
    if current_user.rol.nombre != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden renovar grupos de investigación"
        )
    
    db_grupo = db.query(modelos.GrupoInvestigacion).filter(modelos.GrupoInvestigacion.id == grupo_id).first()
    if db_grupo is None:
        raise HTTPException(status_code=404, detail="Grupo de investigación no encontrado")
    
    db_grupo.fecha_renovacion = datetime.utcnow()
    db_grupo.fecha_vencimiento = fecha_vencimiento
    if observaciones:
        db_grupo.observaciones = observaciones
    db_grupo.fecha_actualizacion = datetime.utcnow()
    
    db.commit()
    db.refresh(db_grupo)
    return db_grupo
