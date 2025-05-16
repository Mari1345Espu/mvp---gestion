from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class Rol(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)

    # Relación con el modelo Usuario
    usuarios = relationship("Usuario", back_populates="rol")

    participantes = relationship("Participante", back_populates="rol")
