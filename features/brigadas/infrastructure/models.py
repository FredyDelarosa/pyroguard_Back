import uuid
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.db.connection import Base

class BrigadistaBrigadaModel(Base):
    __tablename__ = "brigadistas_brigada"
    __table_args__ = {'extend_existing': True}
    
    id_brigada = Column(UUID(as_uuid=True), ForeignKey('brigadas.id_brigada', ondelete="CASCADE"), primary_key=True)
    # User ID is now a loose string (UUID), no foreign key to Auth Service's DB
    id_usuario = Column(String(36), primary_key=True)

class BrigadaModel(Base):
    __tablename__ = "brigadas"
    __table_args__ = {'extend_existing': True}
    
    id_brigada = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(255), nullable=False)
    # Coordinador is a loose string, no foreign key
    id_coordinador = Column(String(36), nullable=True)
    activa = Column(Boolean, default=True)
    creado_en = Column(DateTime, default=func.now())
    
    # Relación a la tabla intermedia
    brigadistas_rel = relationship("BrigadistaBrigadaModel", cascade="all, delete-orphan")
