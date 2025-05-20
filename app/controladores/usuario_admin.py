from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.modelos.usuario import Usuario
from app.modelos.rol import Rol
from app.modelos.estado import Estado
from app.core.seguridad import get_password_hash

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/admin/usuarios", response_class=HTMLResponse)
def listar_usuarios(request: Request, db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    roles = db.query(Rol).all()
    estados = db.query(Estado).all()
    return templates.TemplateResponse("admin/usuarios.html", {"request": request, "usuarios": usuarios, "roles": roles, "estados": estados})

@router.post("/admin/usuarios/crear")
def crear_usuario(
    nombre: str = Form(...),
    correo: str = Form(...),
    contraseña: str = Form(...),
    rol_id: int = Form(...),
    estado_id: int = Form(...),
    db: Session = Depends(get_db)
):
    if db.query(Usuario).filter_by(correo=correo).first():
        return RedirectResponse(url="/admin/usuarios", status_code=status.HTTP_303_SEE_OTHER)
    usuario = Usuario(
        nombre=nombre,
        correo=correo,
        contraseña=get_password_hash(contraseña),
        rol_id=rol_id,
        estado_id=estado_id
    )
    db.add(usuario)
    db.commit()
    return RedirectResponse(url="/admin/usuarios", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/admin/usuarios/editar/{usuario_id}")
def editar_usuario(
    usuario_id: int,
    nombre: str = Form(...),
    correo: str = Form(...),
    rol_id: int = Form(...),
    estado_id: int = Form(...),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario:
        usuario.nombre = nombre
        usuario.correo = correo
        usuario.rol_id = rol_id
        usuario.estado_id = estado_id
        db.commit()
    return RedirectResponse(url="/admin/usuarios", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/admin/usuarios/eliminar/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario:
        db.delete(usuario)
        db.commit()
    return RedirectResponse(url="/admin/usuarios", status_code=status.HTTP_303_SEE_OTHER) 