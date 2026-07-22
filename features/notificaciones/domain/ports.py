from abc import ABC, abstractmethod
from typing import Optional
from features.notificaciones.infrastructure.models import DeviceTokenModel

class DeviceTokenRepository(ABC):
    @abstractmethod
    def save_token(self, id_usuario: str, fcm_token: str) -> DeviceTokenModel:
        pass

    @abstractmethod
    def get_token(self, id_usuario: str) -> Optional[DeviceTokenModel]:
        pass

    @abstractmethod
    def get_all_tokens(self) -> list[DeviceTokenModel]:
        pass
