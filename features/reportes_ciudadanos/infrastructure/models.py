import uuid
from sqlalchemy import Column, String, Float, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from core.db.connection import Base

class ReporteCiudadanoModel(Base):
    __tablename__ = "reportes_ciudadanos"
    __table_args__ = {'extend_existing': True}
    __encrypted_fields__ = ["descripcion"]
    
    id_reporte = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    descripcion = Column(Text, nullable=False)
    latitud = Column(Float, nullable=False)
    longitud = Column(Float, nullable=False)
    foto_url = Column(String(255))
    estado = Column(String(50), default="Pendiente")
    creado_en = Column(DateTime, default=func.now())
