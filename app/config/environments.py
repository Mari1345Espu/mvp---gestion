from pydantic_settings import BaseSettings
from typing import List
from enum import Enum
import os

class Environment(str, Enum):
    """Entornos disponibles."""
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"

class EnvironmentConfig(BaseSettings):
    """Configuración base para todos los entornos."""
    
    # Configuración de la aplicación
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_PREFIX: str = "/api"
    PROJECT_NAME: str = "Sistema de Gestión"
    VERSION: str = "1.0.0"
    
    # Configuración de la base de datos SQLite
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # Configuración de seguridad
    SECRET_KEY: str = "tu_clave_secreta_muy_segura"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Configuración de Redis (opcional para desarrollo)
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""
    
    # Configuración de correo
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = "noreply@tudominio.com"
    
    # Configuración de archivos
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 20 * 1024 * 1024  # 20MB
    
    # Configuración de caché
    CACHE_TTL: int = 300  # 5 minutos
    
    # Configuración de paginación
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 100
    
    # Configuración de CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Configuración de cookies
    COOKIE_SECURE: bool = False
    COOKIE_HTTPONLY: bool = True
    COOKIE_SAMESITE: str = "lax"
    
    # Configuración de rate limiting
    RATE_LIMIT_WINDOW: int = 60  # segundos
    RATE_LIMIT_MAX_REQUESTS: int = 100
    
    # Configuración de logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: str = "logs/app.log"

    class Config:
        env_file = ".env"

def get_environment() -> Environment:
    """Obtiene el entorno actual basado en la variable de entorno APP_ENV."""
    env = os.getenv("APP_ENV", "development")
    return Environment(env)

def get_config() -> EnvironmentConfig:
    """Obtiene la configuración para el entorno actual."""
    env = get_environment()
    return config_by_environment[env]

# Configuraciones específicas por entorno
config_by_environment = {
    Environment.DEVELOPMENT: EnvironmentConfig(
        DEBUG=True,
        DATABASE_URL="sqlite:///./app.db",
        LOG_LEVEL="DEBUG"
    ),
    Environment.TESTING: EnvironmentConfig(
        DEBUG=True,
        DATABASE_URL="sqlite:///./test.db",
        LOG_LEVEL="DEBUG"
    ),
    Environment.STAGING: EnvironmentConfig(
        DEBUG=False,
        DATABASE_URL="sqlite:///./staging.db",
        LOG_LEVEL="INFO"
    ),
    Environment.PRODUCTION: EnvironmentConfig(
        DEBUG=False,
        DATABASE_URL="sqlite:///./prod.db",
        LOG_LEVEL="WARNING"
    )
} 