from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Configuración de la base de datos
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    
    # Configuración de seguridad
    SECRET_KEY: str = os.getenv("SECRET_KEY", "tu_clave_secreta_muy_segura")
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://tudominio.com"
    ]
    
    # Configuración de archivos
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")
    MAX_UPLOAD_SIZE: int = 20 * 1024 * 1024  # 20MB
    
    # Configuración de correo
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    
    # Configuración de seguridad adicional
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    # Configuración de rate limiting
    RATE_LIMIT_WINDOW: int = 60  # segundos
    RATE_LIMIT_MAX_REQUESTS: int = 100
    
    # Configuración de sesión
    SESSION_COOKIE_SECURE: bool = True
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = "Lax"
    
    # Configuración de CSRF
    CSRF_COOKIE_SECURE: bool = True
    CSRF_COOKIE_HTTPONLY: bool = True
    CSRF_COOKIE_SAMESITE: str = "Lax"
    
    # Configuración de Redis
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")
    
    # Configuración de caché
    CACHE_DEFAULT_TIMEOUT: int = 300  # 5 minutos
    CACHE_DASHBOARD_TIMEOUT: int = 300  # 5 minutos
    CACHE_USER_TIMEOUT: int = 3600  # 1 hora
    CACHE_EXTENSION_TIMEOUT: int = 1800  # 30 minutos
    
    # Configuración de paginación
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # Configuración de optimización de base de datos
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800  # 30 minutos
    
    class Config:
        env_file = ".env"

settings = Settings()

# Crear directorio de uploads si no existe
os.makedirs(settings.UPLOAD_DIR, exist_ok=True) 