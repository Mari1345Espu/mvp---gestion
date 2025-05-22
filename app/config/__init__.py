from .environments import Environment, EnvironmentConfig, get_config, get_environment
import os

# Crear directorios necesarios
os.makedirs("uploads", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Exportar configuración
settings = get_config()

__all__ = ["settings", "Environment", "get_environment", "get_config"] 