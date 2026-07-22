from sqlalchemy import Column, String
from core.db.connection import Base

class DeviceTokenModel(Base):
    __tablename__ = "device_tokens"
    __table_args__ = {'extend_existing': True}
    
    id_usuario = Column(String(36), primary_key=True)
    fcm_token = Column(String(255), nullable=False)
