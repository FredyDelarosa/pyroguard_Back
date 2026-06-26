from sqlalchemy import Column, String, Boolean, DateTime, Float, Text, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from core.db.connection import Base

# ==========================================
# MODELOS SQLAlchemy
# ==========================================

# Tabla intermedia N a M para Brigadistas en Brigadas
brigadistas_brigada = Table(
    'brigadistas_brigada',
    Base.metadata,
    Column('id_brigada', UUID(as_uuid=True), ForeignKey('brigadas.id_brigada', ondelete="CASCADE"), primary_key=True),
    Column('id_usuario', UUID(as_uuid=True), ForeignKey('usuarios.id_usuario', ondelete="CASCADE"), primary_key=True)
)

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id_usuario = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    rol = Column(String(50), nullable=False)
    activo = Column(Boolean, default=True)
    creado_en = Column(DateTime, default=func.now())

    brigadas_coordinadas = relationship("Brigada", back_populates="coordinador")

class Brigada(Base):
    __tablename__ = "brigadas"
    
    id_brigada = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(255), nullable=False)
    id_coordinador = Column(UUID(as_uuid=True), ForeignKey('usuarios.id_usuario', ondelete="SET NULL"))
    activa = Column(Boolean, default=True)
    creado_en = Column(DateTime, default=func.now())
    
    coordinador = relationship("Usuario", back_populates="brigadas_coordinadas")
    brigadistas = relationship("Usuario", secondary=brigadistas_brigada)
    intervenciones = relationship("Intervencion", back_populates="brigada")

class Intervencion(Base):
    __tablename__ = "intervenciones"
    
    id_intervencion = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_brigada = Column(UUID(as_uuid=True), ForeignKey('brigadas.id_brigada', ondelete="RESTRICT"))
    id_zona = Column(UUID(as_uuid=True), nullable=False) # Referencia al microservicio de ML
    estado = Column(String(50), nullable=False) # Pendiente, En Progreso, Completada
    observaciones = Column(Text)
    fecha_asignacion = Column(DateTime, default=func.now())
    fecha_completada = Column(DateTime)
    
    brigada = relationship("Brigada", back_populates="intervenciones")

class ReporteCiudadano(Base):
    __tablename__ = "reportes_ciudadanos"
    
    id_reporte = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    descripcion = Column(Text, nullable=False)
    latitud = Column(Float, nullable=False)
    longitud = Column(Float, nullable=False)
    foto_url = Column(String(255))
    estado = Column(String(50), default="Pendiente")
    creado_en = Column(DateTime, default=func.now())

class Comunicado(Base):
    __tablename__ = "comunicados"
    
    id_comunicado = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titulo = Column(String(255), nullable=False)
    contenido = Column(Text, nullable=False)
    id_autor = Column(UUID(as_uuid=True), ForeignKey('usuarios.id_usuario', ondelete="SET NULL"))
    fecha_publicacion = Column(DateTime, default=func.now())
    fecha_vigencia = Column(DateTime, nullable=False)
    
    autor = relationship("Usuario")

class ReporteTecnico(Base):
    __tablename__ = "reportes_tecnicos"
    
    id_reporte = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_zona = Column(UUID(as_uuid=True), nullable=False)
    id_coordinador = Column(UUID(as_uuid=True), ForeignKey('usuarios.id_usuario', ondelete="SET NULL"))
    nivel_riesgo_registrado = Column(String(50))
    archivo_pdf_path = Column(String(255))
    creado_en = Column(DateTime, default=func.now())
    
    coordinador = relationship("Usuario")

class ObservacionCampo(Base):
    __tablename__ = "observaciones_campo"
    
    id_observacion = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_brigadista = Column(UUID(as_uuid=True), ForeignKey('usuarios.id_usuario', ondelete="SET NULL"))
    id_zona = Column(UUID(as_uuid=True), nullable=False) # Referencia a zona en ML
    latitud = Column(Float, nullable=False)
    longitud = Column(Float, nullable=False)
    condiciones = Column(String(100), nullable=False) # e.g., Favorable, Peligro, Inaccesible
    recursos_necesarios = Column(String(255))
    observaciones_texto = Column(Text)
    creado_en = Column(DateTime, default=func.now())
    
    brigadista = relationship("Usuario")
