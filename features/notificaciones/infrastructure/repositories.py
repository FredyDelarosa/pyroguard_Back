from sqlalchemy.orm import Session
from typing import Optional
from features.notificaciones.domain.ports import DeviceTokenRepository
from features.notificaciones.infrastructure.models import DeviceTokenModel

class DeviceTokenRepositoryImpl(DeviceTokenRepository):
    def __init__(self, db: Session):
        self.db = db
        
    def save_token(self, id_usuario: str, fcm_token: str) -> DeviceTokenModel:
        token_db = self.db.query(DeviceTokenModel).filter(DeviceTokenModel.id_usuario == id_usuario).first()
        if token_db:
            token_db.fcm_token = fcm_token
        else:
            token_db = DeviceTokenModel(id_usuario=id_usuario, fcm_token=fcm_token)
            self.db.add(token_db)
        
        self.db.commit()
        self.db.refresh(token_db)
        return token_db

    def get_token(self, id_usuario: str) -> Optional[DeviceTokenModel]:
        return self.db.query(DeviceTokenModel).filter(DeviceTokenModel.id_usuario == id_usuario).first()

    def get_all_tokens(self) -> list[DeviceTokenModel]:
        return self.db.query(DeviceTokenModel).all()
