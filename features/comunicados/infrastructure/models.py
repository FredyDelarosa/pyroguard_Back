import uuid
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from core.db.connection import Base

class ComunicadoModel(Base):
    __tablename__ = "comunicados"
    __table_args__ = {'extend_existing': True}
    
    id_comunicado = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titulo = Column(String(255), nullable=False)
    contenido = Column(Text, nullable=False)
    id_autor = Column(String(36), nullable=True)
    fecha_publicacion = Column(DateTime, default=func.now())
    fecha_vigencia = Column(DateTime, nullable=False)