import uuid
from sqlalchemy import Column, String, Float, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from core.db.connection import Base

class ObservacionCampoModel(Base):
    __tablename__ = "observaciones_campo"
    __table_args__ = {'extend_existing': True}
    
    id_observacion = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_brigadista = Column(String(36), nullable=True)
    id_zona = Column(UUID(as_uuid=True), nullable=False)
    latitud = Column(Float, nullable=False)
    longitud = Column(Float, nullable=False)
    condiciones = Column(String(100), nullable=False)
    recursos_necesarios = Column(String(255))
    observaciones_texto = Column(Text)
    creado_en = Column(DateTime, default=func.now())