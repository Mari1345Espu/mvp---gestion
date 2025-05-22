from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import joinedload, selectinload, contains_eager
from sqlalchemy.sql import text
from typing import List, Optional, Any, Dict
from ..database import SessionLocal
from ..config import settings

class QueryOptimizer:
    """Optimizador de consultas a base de datos."""
    
    @staticmethod
    def paginate_query(
        query,
        page: int = 1,
        per_page: int = 20,
        max_per_page: int = 100
    ):
        """
        Aplica paginación a una consulta.
        
        Args:
            query: Consulta SQLAlchemy
            page: Número de página
            per_page: Elementos por página
            max_per_page: Máximo de elementos por página
        """
        # Validar y ajustar parámetros
        page = max(1, page)
        per_page = min(max(1, per_page), max_per_page)
        
        # Calcular offset
        offset = (page - 1) * per_page
        
        # Aplicar paginación
        return query.offset(offset).limit(per_page)
    
    @staticmethod
    def eager_load_relations(
        query,
        relations: List[str],
        strategy: str = "joined"
    ):
        """
        Carga eager de relaciones para evitar N+1 queries.
        
        Args:
            query: Consulta SQLAlchemy
            relations: Lista de relaciones a cargar
            strategy: Estrategia de carga ('joined', 'selectin', 'subquery')
        """
        load_strategies = {
            "joined": joinedload,
            "selectin": selectinload,
            "subquery": contains_eager
        }
        
        load_strategy = load_strategies.get(strategy, joinedload)
        
        for relation in relations:
            query = query.options(load_strategy(relation))
        
        return query
    
    @staticmethod
    def optimize_count_query(query):
        """
        Optimiza una consulta de conteo.
        
        Args:
            query: Consulta SQLAlchemy
        """
        return query.with_only_columns([func.count()]).scalar()
    
    @staticmethod
    def add_search_filter(
        query,
        model,
        search_term: str,
        search_fields: List[str]
    ):
        """
        Agrega filtro de búsqueda a una consulta.
        
        Args:
            query: Consulta SQLAlchemy
            model: Modelo SQLAlchemy
            search_term: Término de búsqueda
            search_fields: Campos a buscar
        """
        if not search_term:
            return query
        
        search_conditions = []
        for field in search_fields:
            column = getattr(model, field)
            search_conditions.append(column.ilike(f"%{search_term}%"))
        
        return query.filter(or_(*search_conditions))
    
    @staticmethod
    def add_date_range_filter(
        query,
        model,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        date_field: str = "fecha_creacion"
    ):
        """
        Agrega filtro de rango de fechas a una consulta.
        
        Args:
            query: Consulta SQLAlchemy
            model: Modelo SQLAlchemy
            start_date: Fecha inicial
            end_date: Fecha final
            date_field: Campo de fecha
        """
        conditions = []
        date_column = getattr(model, date_field)
        
        if start_date:
            conditions.append(date_column >= start_date)
        if end_date:
            conditions.append(date_column <= end_date)
        
        if conditions:
            return query.filter(and_(*conditions))
        
        return query

class DatabaseOptimizer:
    """Optimizador de base de datos."""
    
    @staticmethod
    def create_indexes():
        """Crea índices para optimizar consultas frecuentes."""
        with SessionLocal() as db:
            # Índices para usuarios
            db.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_usuarios_correo 
                ON usuarios(correo);
            """))
            
            # Índices para extensiones
            db.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_extensiones_fecha 
                ON extensiones(fecha_creacion);
            """))
            
            # Índices para seguimientos
            db.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_seguimientos_extension 
                ON seguimientos(extension_id);
            """))
            
            # Índices para impactos
            db.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_impactos_tipo 
                ON impactos(tipo);
            """))
            
            db.commit()
    
    @staticmethod
    def vacuum_database():
        """Ejecuta VACUUM para optimizar el espacio en disco."""
        with SessionLocal() as db:
            db.execute(text("VACUUM;"))
            db.commit()
    
    @staticmethod
    def analyze_tables():
        """Ejecuta ANALYZE para actualizar estadísticas de tablas."""
        with SessionLocal() as db:
            db.execute(text("ANALYZE;"))
            db.commit()
    
    @staticmethod
    def get_table_stats() -> Dict[str, Any]:
        """Obtiene estadísticas de las tablas."""
        with SessionLocal() as db:
            result = db.execute(text("""
                SELECT 
                    relname as table_name,
                    n_live_tup as row_count,
                    pg_size_pretty(pg_total_relation_size(relid)) as total_size
                FROM pg_stat_user_tables
                ORDER BY n_live_tup DESC;
            """))
            
            return {
                row.table_name: {
                    "row_count": row.row_count,
                    "total_size": row.total_size
                }
                for row in result
            } 