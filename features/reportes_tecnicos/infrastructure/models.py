import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from core.db.connection import Base

class ReporteTecnicoModel(Base):
    __tablename__ = "reportes_tecnicos"
    __table_args__ = {'extend_existing': True}
    
    id_reporte = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_zona = Column(UUID(as_uuid=True), nullable=False)
    id_coordinador = Column(String(36), nullable=True)
    nivel_riesgo_registrado = Column(String(50))
    archivo_pdf_path = Column(String(255))
    creado_en = Column(DateTime, default=func.now())