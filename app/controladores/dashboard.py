from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, Any, List
from datetime import datetime, timedelta

from app import modelos
from app.db.session import get_db
from app.core.seguridad import get_current_user

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard_data(
    current_user: modelos.Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene los datos del dashboard según el rol del usuario
    """
    try:
        if not current_user.rol:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario sin rol asignado"
            )

        # Datos comunes para todos los roles
        common_data = {
            "total_proyectos": db.query(func.count(modelos.Proyecto.id)).scalar() or 0,
            "proyectos_activos": db.query(func.count(modelos.Proyecto.id))
                .filter(modelos.Proyecto.estado_id == 1)  # Asumiendo que 1 es el ID del estado "Activo"
                .scalar() or 0,
            "proyectos_completados": db.query(func.count(modelos.Proyecto.id))
                .filter(modelos.Proyecto.estado_id == 2)  # Asumiendo que 2 es el ID del estado "Completado"
                .scalar() or 0
        }

        # Datos específicos según el rol
        role_data = {}
        
        if current_user.rol.nombre == "Administrador":
            role_data = {
                "admin": {
                    "total_usuarios": db.query(func.count(modelos.Usuario.id)).scalar() or 0,
                    "usuarios_activos": db.query(func.count(modelos.Usuario.id))
                        .filter(modelos.Usuario.estado_id == 1)
                        .scalar() or 0,
                    "usuarios_inactivos": db.query(func.count(modelos.Usuario.id))
                        .filter(modelos.Usuario.estado_id == 2)
                        .scalar() or 0
                }
            }
        elif current_user.rol.nombre == "Líder de Grupo":
            grupo = db.query(modelos.GrupoInvestigacion).filter(
                modelos.GrupoInvestigacion.lider_id == current_user.id
            ).first()
            
            if grupo:
                role_data = {
                    "group_leader": {
                        "grupos_activos": 1,  # El grupo del líder
                        "total_investigadores": db.query(func.count(modelos.Usuario.id))
                            .filter(modelos.Usuario.grupo_id == grupo.id)
                            .scalar() or 0,
                        "proyectos_por_grupo": db.query(func.count(modelos.Proyecto.id))
                            .filter(modelos.Proyecto.grupo_id == grupo.id)
                            .scalar() or 0
                    }
                }
        elif current_user.rol.nombre == "Investigador":
            role_data = {
                "researcher": {
                    "proyectos_asignados": db.query(func.count(modelos.Proyecto.id))
                        .filter(modelos.Proyecto.investigadores.any(id=current_user.id))
                        .scalar() or 0,
                    "tareas_pendientes": db.query(func.count(modelos.Tarea.id))
                        .filter(
                            modelos.Tarea.responsable_id == current_user.id,
                            modelos.Tarea.estado_id == 1
                        )
                        .scalar() or 0,
                    "tareas_completadas": db.query(func.count(modelos.Tarea.id))
                        .filter(
                            modelos.Tarea.responsable_id == current_user.id,
                            modelos.Tarea.estado_id == 2
                        )
                        .scalar() or 0
                }
            }
        elif current_user.rol.nombre in ["Evaluador Interno", "Evaluador Externo"]:
            evaluador_field = "evaluador_id" if current_user.rol.nombre == "Evaluador Interno" else "evaluador_externo_id"
            
            role_data = {
                "evaluator": {
                    "evaluaciones_pendientes": db.query(func.count(modelos.Evaluacion.id))
                        .filter(
                            getattr(modelos.Evaluacion, evaluador_field) == current_user.id,
                            modelos.Evaluacion.estado == "Pendiente"
                        )
                        .scalar() or 0,
                    "evaluaciones_completadas": db.query(func.count(modelos.Evaluacion.id))
                        .filter(
                            getattr(modelos.Evaluacion, evaluador_field) == current_user.id,
                            modelos.Evaluacion.estado == "Completada"
                        )
                        .scalar() or 0,
                    "proyectos_evaluados": db.query(func.count(modelos.Evaluacion.id))
                        .filter(
                            getattr(modelos.Evaluacion, evaluador_field) == current_user.id,
                            modelos.Evaluacion.estado == "Completada"
                        )
                        .scalar() or 0
                }
            }

        return {
            "user": {
                "id": current_user.id,
                "nombre": current_user.nombre,
                "correo": current_user.correo,
                "rol_nombre": current_user.rol.nombre
            },
            "common": common_data,
            **role_data
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

async def get_role_specific_data(user: modelos.Usuario, db: Session) -> Dict[str, Any]:
    """
    Obtiene datos específicos según el rol del usuario
    """
    try:
        if user.rol.nombre == "Administrador":
            return {
                "administrador": {
                    "total_usuarios": db.query(func.count(modelos.Usuario.id)).scalar() or 0,
                    "grupos_activos": db.query(func.count(modelos.GrupoInvestigacion.id))
                        .filter(modelos.GrupoInvestigacion.estado_id == 1)  # Asumiendo que 1 es el ID del estado "Activo"
                        .scalar() or 0
                }
            }
        elif user.rol.nombre == "Líder de Grupo":
            grupo = db.query(modelos.GrupoInvestigacion).filter(
                modelos.GrupoInvestigacion.lider_id == user.id
            ).first()
            
            if not grupo:
                return {
                    "lider_grupo": {
                        "miembros_grupo": 0,
                        "proyectos_grupo": 0
                    }
                }
            
            return {
                "lider_grupo": {
                    "miembros_grupo": db.query(func.count(modelos.Usuario.id))
                        .filter(modelos.Usuario.grupo_id == grupo.id)
                        .scalar() or 0,
                    "proyectos_grupo": db.query(func.count(modelos.Proyecto.id))
                        .filter(modelos.Proyecto.grupo_id == grupo.id)
                        .scalar() or 0
                }
            }
        elif user.rol.nombre == "Investigador":
            return {
                "investigador": {
                    "proyectos_asignados": db.query(func.count(modelos.Proyecto.id))
                        .filter(modelos.Proyecto.investigadores.any(id=user.id))
                        .scalar() or 0,
                    "tareas_pendientes": db.query(func.count(modelos.Tarea.id))
                        .filter(
                            modelos.Tarea.responsable_id == user.id,
                            modelos.Tarea.estado_id == 1  # Asumiendo que 1 es el ID del estado "Pendiente"
                        )
                        .scalar() or 0
                }
            }
        elif user.rol.nombre in ["Evaluador Interno", "Evaluador Externo"]:
            evaluador_field = "evaluador_id" if user.rol.nombre == "Evaluador Interno" else "evaluador_externo_id"
            
            return {
                "evaluador": {
                    "proyectos_por_evaluar": db.query(func.count(modelos.Evaluacion.id))
                        .filter(
                            getattr(modelos.Evaluacion, evaluador_field) == user.id,
                            modelos.Evaluacion.estado == "Pendiente"
                        )
                        .scalar() or 0,
                    "evaluaciones_completadas": db.query(func.count(modelos.Evaluacion.id))
                        .filter(
                            getattr(modelos.Evaluacion, evaluador_field) == user.id,
                            modelos.Evaluacion.estado == "Completada"
                        )
                        .scalar() or 0
                }
            }
        else:
            return {}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener datos específicos del rol: {str(e)}"
        )

@router.get("/dashboard/cards")
async def get_dashboard_cards(
    current_user: modelos.Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene las cards del dashboard según el rol del usuario
    """
    try:
        if not current_user.rol:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario sin rol asignado"
            )

        # Cards comunes para todos los roles
        common_cards = [
            {
                "title": "Proyectos",
                "icon": "assignment",
                "items": [
                    {
                        "label": "Total",
                        "value": db.query(func.count(modelos.Proyecto.id)).scalar() or 0
                    },
                    {
                        "label": "Activos",
                        "value": db.query(func.count(modelos.Proyecto.id))
                            .filter(modelos.Proyecto.estado_id == 1)
                            .scalar() or 0
                    },
                    {
                        "label": "Completados",
                        "value": db.query(func.count(modelos.Proyecto.id))
                            .filter(modelos.Proyecto.estado_id == 2)
                            .scalar() or 0
                    }
                ]
            }
        ]

        # Cards específicas según el rol
        role_cards = []
        
        if current_user.rol.nombre == "Administrador":
            role_cards = [
                {
                    "title": "Usuarios",
                    "icon": "people",
                    "items": [
                        {
                            "label": "Total",
                            "value": db.query(func.count(modelos.Usuario.id)).scalar() or 0
                        },
                        {
                            "label": "Activos",
                            "value": db.query(func.count(modelos.Usuario.id))
                                .filter(modelos.Usuario.estado_id == 1)
                                .scalar() or 0
                        },
                        {
                            "label": "Inactivos",
                            "value": db.query(func.count(modelos.Usuario.id))
                                .filter(modelos.Usuario.estado_id == 2)
                                .scalar() or 0
                        }
                    ]
                },
                {
                    "title": "Grupos de Investigación",
                    "icon": "groups",
                    "items": [
                        {
                            "label": "Total",
                            "value": db.query(func.count(modelos.GrupoInvestigacion.id)).scalar() or 0
                        },
                        {
                            "label": "Activos",
                            "value": db.query(func.count(modelos.GrupoInvestigacion.id))
                                .filter(modelos.GrupoInvestigacion.estado_id == 1)
                                .scalar() or 0
                        }
                    ]
                }
            ]
        elif current_user.rol.nombre == "Líder de Grupo":
            grupo = db.query(modelos.GrupoInvestigacion).filter(
                modelos.GrupoInvestigacion.lider_id == current_user.id
            ).first()
            
            if grupo:
                role_cards = [
                    {
                        "title": "Mi Grupo",
                        "icon": "group",
                        "items": [
                            {
                                "label": "Investigadores",
                                "value": db.query(func.count(modelos.Usuario.id))
                                    .filter(modelos.Usuario.grupo_id == grupo.id)
                                    .scalar() or 0
                            },
                            {
                                "label": "Proyectos",
                                "value": db.query(func.count(modelos.Proyecto.id))
                                    .filter(modelos.Proyecto.grupo_id == grupo.id)
                                    .scalar() or 0
                            }
                        ]
                    }
                ]
        elif current_user.rol.nombre == "Investigador":
            role_cards = [
                {
                    "title": "Mis Proyectos",
                    "icon": "science",
                    "items": [
                        {
                            "label": "Asignados",
                            "value": db.query(func.count(modelos.Proyecto.id))
                                .filter(modelos.Proyecto.investigadores.any(id=current_user.id))
                                .scalar() or 0
                        }
                    ]
                },
                {
                    "title": "Mis Tareas",
                    "icon": "task",
                    "items": [
                        {
                            "label": "Pendientes",
                            "value": db.query(func.count(modelos.Tarea.id))
                                .filter(
                                    modelos.Tarea.responsable_id == current_user.id,
                                    modelos.Tarea.estado_id == 1
                                )
                                .scalar() or 0
                        },
                        {
                            "label": "Completadas",
                            "value": db.query(func.count(modelos.Tarea.id))
                                .filter(
                                    modelos.Tarea.responsable_id == current_user.id,
                                    modelos.Tarea.estado_id == 2
                                )
                                .scalar() or 0
                        }
                    ]
                }
            ]
        elif current_user.rol.nombre in ["Evaluador Interno", "Evaluador Externo"]:
            evaluador_field = "evaluador_id" if current_user.rol.nombre == "Evaluador Interno" else "evaluador_externo_id"
            
            role_cards = [
                {
                    "title": "Evaluaciones",
                    "icon": "rate_review",
                    "items": [
                        {
                            "label": "Pendientes",
                            "value": db.query(func.count(modelos.Evaluacion.id))
                                .filter(
                                    getattr(modelos.Evaluacion, evaluador_field) == current_user.id,
                                    modelos.Evaluacion.estado == "Pendiente"
                                )
                                .scalar() or 0
                        },
                        {
                            "label": "Completadas",
                            "value": db.query(func.count(modelos.Evaluacion.id))
                                .filter(
                                    getattr(modelos.Evaluacion, evaluador_field) == current_user.id,
                                    modelos.Evaluacion.estado == "Completada"
                                )
                                .scalar() or 0
                        }
                    ]
                }
            ]

        return {
            "user": {
                "id": current_user.id,
                "nombre": current_user.nombre,
                "correo": current_user.correo,
                "rol_nombre": current_user.rol.nombre
            },
            "cards": common_cards + role_cards
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 