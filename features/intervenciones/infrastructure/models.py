import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from core.db.connection import Base

class IntervencionModel(Base):
    __tablename__ = "intervenciones"
    __table_args__ = {'extend_existing': True}
    
    id_intervencion = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_brigada = Column(UUID(as_uuid=True), ForeignKey('brigadas.id_brigada', ondelete="RESTRICT"))
    id_zona = Column(UUID(as_uuid=True), nullable=False)
    estado = Column(String(50), nullable=False)
    observaciones = Column(Text)
    fecha_asignacion = Column(DateTime, default=func.now())
    fecha_completada = Column(DateTime)