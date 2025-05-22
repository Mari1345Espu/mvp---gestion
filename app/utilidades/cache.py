from functools import wraps
from typing import Any, Callable, Optional
import json
from datetime import datetime, timedelta
import redis
from ..config import settings

# Configuración de Redis
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)

def cache(
    expire: int = 300,  # 5 minutos por defecto
    key_prefix: str = "",
    include_args: bool = True
):
    """
    Decorador para cachear resultados de funciones.
    
    Args:
        expire: Tiempo de expiración en segundos
        key_prefix: Prefijo para la clave de caché
        include_args: Si se deben incluir los argumentos en la clave
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            # Generar clave de caché
            cache_key = f"{key_prefix}:{func.__name__}"
            if include_args:
                args_key = ":".join(str(arg) for arg in args)
                kwargs_key = ":".join(f"{k}={v}" for k, v in sorted(kwargs.items()))
                if args_key:
                    cache_key += f":{args_key}"
                if kwargs_key:
                    cache_key += f":{kwargs_key}"
            
            # Intentar obtener de caché
            cached_value = redis_client.get(cache_key)
            if cached_value:
                return json.loads(cached_value)
            
            # Ejecutar función si no está en caché
            result = await func(*args, **kwargs)
            
            # Guardar en caché
            redis_client.setex(
                cache_key,
                expire,
                json.dumps(result)
            )
            
            return result
        return wrapper
    return decorator

def invalidate_cache(pattern: str) -> None:
    """
    Invalida todas las claves de caché que coincidan con el patrón.
    
    Args:
        pattern: Patrón de claves a invalidar (ej: "user:*")
    """
    keys = redis_client.keys(pattern)
    if keys:
        redis_client.delete(*keys)

class CacheManager:
    """Gestor de caché para la aplicación."""
    
    @staticmethod
    def cache_dashboard(expire: int = 300):
        """Cachea datos del dashboard."""
        return cache(
            expire=expire,
            key_prefix="dashboard",
            include_args=False
        )
    
    @staticmethod
    def cache_user_data(expire: int = 3600):
        """Cachea datos de usuario."""
        return cache(
            expire=expire,
            key_prefix="user",
            include_args=True
        )
    
    @staticmethod
    def cache_extension_data(expire: int = 1800):
        """Cachea datos de extensiones."""
        return cache(
            expire=expire,
            key_prefix="extension",
            include_args=True
        )
    
    @staticmethod
    def invalidate_user_cache(user_id: int) -> None:
        """Invalida caché de un usuario."""
        invalidate_cache(f"user:{user_id}:*")
    
    @staticmethod
    def invalidate_extension_cache(extension_id: int) -> None:
        """Invalida caché de una extensión."""
        invalidate_cache(f"extension:{extension_id}:*")
    
    @staticmethod
    def invalidate_dashboard_cache() -> None:
        """Invalida caché del dashboard."""
        invalidate_cache("dashboard:*") 