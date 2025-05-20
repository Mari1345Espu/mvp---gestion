from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.core.seguridad import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard_redirect(request: Request, user=Depends(get_current_user)):
    if user.rol and user.rol.nombre == "Administrador":
        return RedirectResponse("/admin/dashboard")
    elif user.rol and user.rol.nombre == "Líder de Grupo":
        return RedirectResponse("/lider/dashboard")
    elif user.rol and user.rol.nombre == "Investigador":
        return RedirectResponse("/investigador/dashboard")
    elif user.rol and user.rol.nombre == "Evaluador":
        return RedirectResponse("/evaluador/dashboard")
    else:
        return RedirectResponse("/usuario/dashboard")

@router.get("/admin/dashboard", response_class=HTMLResponse)
def dashboard_admin(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("admin/dashboard.html", {"request": request, "user": user})

@router.get("/lider/dashboard", response_class=HTMLResponse)
def dashboard_lider(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("lider/dashboard.html", {"request": request, "user": user})

@router.get("/investigador/dashboard", response_class=HTMLResponse)
def dashboard_investigador(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("investigador/dashboard.html", {"request": request, "user": user})

@router.get("/evaluador/dashboard", response_class=HTMLResponse)
def dashboard_evaluador(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("evaluador/dashboard.html", {"request": request, "user": user})

@router.get("/usuario/dashboard", response_class=HTMLResponse)
def dashboard_usuario(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("usuario/dashboard.html", {"request": request, "user": user}) 