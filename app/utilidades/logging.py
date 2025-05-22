import logging
import sys
from logging.handlers import RotatingFileHandler
import json
from datetime import datetime
from typing import Any, Dict
import os
from ..config import settings
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp, Receive, Scope, Send

# Configuración de directorios
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

class JSONFormatter(logging.Formatter):
    """Formateador personalizado para logs en formato JSON."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Formatea el registro de log como JSON."""
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Agregar excepción si existe
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": self.formatException(record.exc_info)
            }
        
        # Agregar datos adicionales si existen
        if hasattr(record, "extra_data"):
            log_data["extra_data"] = record.extra_data
            
        return json.dumps(log_data)

def setup_logging() -> None:
    """Configura el sistema de logging."""
    # Crear logger principal
    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)
    
    # Limpiar handlers existentes
    logger.handlers = []
    
    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    
    # Handler para archivo (formato JSON)
    file_handler = RotatingFileHandler(
        filename=os.path.join(LOG_DIR, "app.log"),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(JSONFormatter())
    
    # Agregar handlers al logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    # Configurar logging para otras bibliotecas
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)

def get_logger(name: str) -> logging.Logger:
    """Obtiene un logger configurado."""
    return logging.getLogger(f"app.{name}")

class RequestLogger(BaseHTTPMiddleware):
    """Middleware para logging de requests."""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.logger = get_logger("requests")
    
    async def dispatch(self, request, call_next):
        # Log de inicio de request
        start_time = datetime.utcnow()
        request_id = request.headers.get("X-Request-ID", "unknown")
        
        self.logger.info(
            "Request iniciado",
            extra={
                "request_id": request_id,
                "method": request.method,
                "url": str(request.url),
                "client_ip": request.client.host,
                "user_agent": request.headers.get("user-agent")
            }
        )
        
        try:
            response = await call_next(request)
            
            # Log de fin de request
            process_time = (datetime.utcnow() - start_time).total_seconds()
            self.logger.info(
                "Request completado",
                extra={
                    "request_id": request_id,
                    "status_code": response.status_code,
                    "process_time": process_time
                }
            )
            
            return response
            
        except Exception as e:
            # Log de error
            self.logger.error(
                "Error en request",
                exc_info=True,
                extra={
                    "request_id": request_id,
                    "error": str(e)
                }
            )
            raise 