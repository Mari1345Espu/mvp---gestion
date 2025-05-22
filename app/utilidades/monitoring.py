from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import Request, Response
import time
from typing import Callable
import psutil
import os
from ..config import settings
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp, Receive, Scope, Send

# Métricas de requests
REQUEST_COUNT = Counter(
    'app_request_count',
    'Número total de requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'app_request_latency_seconds',
    'Latencia de requests en segundos',
    ['method', 'endpoint']
)

# Métricas de errores
ERROR_COUNT = Counter(
    'app_error_count',
    'Número total de errores',
    ['type', 'endpoint']
)

# Métricas de sistema
CPU_USAGE = Gauge(
    'app_cpu_usage_percent',
    'Uso de CPU en porcentaje'
)

MEMORY_USAGE = Gauge(
    'app_memory_usage_bytes',
    'Uso de memoria en bytes'
)

DISK_USAGE = Gauge(
    'app_disk_usage_bytes',
    'Uso de disco en bytes'
)

# Métricas de base de datos
DB_CONNECTIONS = Gauge(
    'app_db_connections',
    'Número de conexiones activas a la base de datos'
)

DB_QUERY_TIME = Histogram(
    'app_db_query_time_seconds',
    'Tiempo de ejecución de queries en segundos'
)

class MonitoringMiddleware(BaseHTTPMiddleware):
    """Middleware para monitoreo de la aplicación."""
    
    async def dispatch(self, request: Request, call_next):
        # Métricas de sistema
        CPU_USAGE.set(psutil.cpu_percent())
        MEMORY_USAGE.set(psutil.Process().memory_info().rss)
        DISK_USAGE.set(psutil.disk_usage('/').used)
        
        # Métricas de request
        start_time = time.time()
        path = request.url.path
        
        try:
            response = await call_next(request)
            
            # Registrar métricas de request
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=path,
                status=response.status_code
            ).inc()
            
            REQUEST_LATENCY.labels(
                method=request.method,
                endpoint=path
            ).observe(time.time() - start_time)
            
            return response
            
        except Exception as e:
            # Registrar error
            ERROR_COUNT.labels(
                type=type(e).__name__,
                endpoint=path
            ).inc()
            raise

def get_metrics():
    """Endpoint para obtener métricas en formato Prometheus."""
    return Response(
        generate_latest(),
        media_type="text/plain"
    )

class DatabaseMonitor:
    """Monitor para métricas de base de datos."""
    
    def __init__(self, engine):
        self.engine = engine
    
    def update_metrics(self):
        """Actualiza métricas de base de datos."""
        # Obtener número de conexiones activas
        with self.engine.connect() as conn:
            result = conn.execute("SELECT count(*) FROM pg_stat_activity")
            active_connections = result.scalar()
            DB_CONNECTIONS.set(active_connections)
    
    def track_query_time(self, query_time: float):
        """Registra tiempo de ejecución de query."""
        DB_QUERY_TIME.observe(query_time)

def setup_monitoring(app, engine=None):
    """Configura el monitoreo de la aplicación."""
    # Agregar middleware de monitoreo
    app.add_middleware(MonitoringMiddleware)
    
    # Agregar endpoint de métricas
    app.get("/metrics")(get_metrics)
    
    # Configurar monitor de base de datos si hay engine
    if engine:
        db_monitor = DatabaseMonitor(engine)
        return db_monitor
    
    return None 