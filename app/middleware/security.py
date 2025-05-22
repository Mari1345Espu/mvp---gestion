from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Callable
import re
import time
from collections import defaultdict
import bleach
import json
from ..config import settings

# Configuración de rate limiting
RATE_LIMIT_WINDOW = 60  # segundos
RATE_LIMIT_MAX_REQUESTS = 100  # máximo de peticiones por ventana
RATE_LIMIT_BY_IP = defaultdict(lambda: {"count": 0, "window_start": time.time()})

# Configuración de CSRF
CSRF_TOKEN_HEADER = "X-CSRF-Token"
CSRF_TOKEN_COOKIE = "csrf_token"

# Lista de dominios permitidos para CORS
ALLOWED_ORIGINS = settings.ALLOWED_ORIGINS

# Tipos de archivos permitidos para upload
ALLOWED_FILE_TYPES = {
    "image": ["image/jpeg", "image/png", "image/gif"],
    "document": ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"],
    "spreadsheet": ["application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"],
    "presentation": ["application/vnd.ms-powerpoint", "application/vnd.openxmlformats-officedocument.presentationml.presentation"]
}

async def validate_csrf_token(request: Request) -> None:
    """Valida el token CSRF."""
    if request.method in ["GET", "HEAD", "OPTIONS"]:
        return

    csrf_token = request.headers.get(CSRF_TOKEN_HEADER)
    csrf_cookie = request.cookies.get(CSRF_TOKEN_COOKIE)

    if not csrf_token or not csrf_cookie or csrf_token != csrf_cookie:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token CSRF inválido"
        )

async def rate_limit_middleware(request: Request) -> None:
    """Implementa rate limiting por IP."""
    client_ip = request.client.host
    current_time = time.time()
    
    # Limpiar ventanas antiguas
    if current_time - RATE_LIMIT_BY_IP[client_ip]["window_start"] > RATE_LIMIT_WINDOW:
        RATE_LIMIT_BY_IP[client_ip] = {"count": 0, "window_start": current_time}
    
    # Incrementar contador
    RATE_LIMIT_BY_IP[client_ip]["count"] += 1
    
    # Verificar límite
    if RATE_LIMIT_BY_IP[client_ip]["count"] > RATE_LIMIT_MAX_REQUESTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Demasiadas peticiones. Por favor, intente más tarde."
        )

def sanitize_input(data: str) -> str:
    """Sanitiza el input para prevenir XSS."""
    return bleach.clean(data, strip=True)

def validate_file_type(content_type: str, file_type: str) -> bool:
    """Valida el tipo de archivo."""
    return content_type in ALLOWED_FILE_TYPES.get(file_type, [])

async def security_middleware(request: Request, call_next: Callable) -> JSONResponse:
    """Middleware principal de seguridad."""
    try:
        # Validar CSRF
        await validate_csrf_token(request)
        
        # Rate limiting
        await rate_limit_middleware(request)
        
        # Sanitizar headers
        for key, value in request.headers.items():
            if isinstance(value, str):
                request.headers[key] = sanitize_input(value)
        
        # Sanitizar query params
        for key, value in request.query_params.items():
            if isinstance(value, str):
                request.query_params[key] = sanitize_input(value)
        
        # Sanitizar body para métodos POST/PUT/PATCH
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.json()
                if isinstance(body, dict):
                    for key, value in body.items():
                        if isinstance(value, str):
                            body[key] = sanitize_input(value)
                    request._body = json.dumps(body).encode()
            except:
                pass
        
        # Validar CORS
        origin = request.headers.get("origin")
        if origin and origin not in ALLOWED_ORIGINS:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Origen no permitido"
            )
        
        response = await call_next(request)
        return response
        
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Error interno del servidor"}
        ) 