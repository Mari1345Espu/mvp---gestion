from db.database import Base, engine
from modelos import *  # Importa todos los modelos

def init_db():
    """Inicializa la base de datos creando todas las tablas."""
    print("Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("¡Base de datos inicializada!")

if __name__ == "__main__":
    init_db() 