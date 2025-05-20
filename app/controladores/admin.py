from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.seguridad import get_current_user_admin

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/admin/dashboard", response_class=HTMLResponse)
async def dashboard_admin(request: Request, user=Depends(get_current_user_admin)):
    return templates.TemplateResponse("admin/dashboard_admin.html", {"request": request, "user": user})

@router.get("/admin/convocatorias", response_class=HTMLResponse)
async def admin_convocatorias(request: Request, user=Depends(get_current_user_admin)):
    return templates.TemplateResponse("admin/convocatorias.html", {"request": request, "user": user})

@router.get("/admin/proyectos", response_class=HTMLResponse)
async def admin_proyectos(request: Request, user=Depends(get_current_user_admin)):
    return templates.TemplateResponse("admin/proyectos.html", {"request": request, "user": user})

@router.get("/admin/investigadores", response_class=HTMLResponse)
async def admin_investigadores(request: Request, user=Depends(get_current_user_admin)):
    return templates.TemplateResponse("admin/investigadores.html", {"request": request, "user": user})

@router.get("/admin/evaluadores", response_class=HTMLResponse)
async def admin_evaluadores(request: Request, user=Depends(get_current_user_admin)):
    return templates.TemplateResponse("admin/evaluadores.html", {"request": request, "user": user})

@router.get("/admin/seguimiento", response_class=HTMLResponse)
async def admin_seguimiento(request: Request, user=Depends(get_current_user_admin)):
    return templates.TemplateResponse("admin/seguimiento.html", {"request": request, "user": user})

@router.get("/admin/reportes", response_class=HTMLResponse)
async def admin_reportes(request: Request, user=Depends(get_current_user_admin)):
    return templates.TemplateResponse("admin/reportes.html", {"request": request, "user": user})

@router.get("/admin/roles", response_class=HTMLResponse)
async def admin_roles(request: Request, user=Depends(get_current_user_admin)):
    return templates.TemplateResponse("admin/roles.html", {"request": request, "user": user})

@router.get("/admin/notificaciones", response_class=HTMLResponse)
async def admin_notificaciones(request: Request, user=Depends(get_current_user_admin)):
    return templates.TemplateResponse("admin/notificaciones.html", {"request": request, "user": user}) 