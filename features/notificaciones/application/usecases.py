from features.notificaciones.domain.ports import DeviceTokenRepository
from features.notificaciones.domain.entities import DeviceTokenCreate, DeviceTokenResponse, AlertaCriticidadRequest
from core.clients.implementations.firebase_client import firebase_client
from typing import Optional

class NotificacionesUseCase:
    def __init__(self, repo: DeviceTokenRepository):
        self.repo = repo
        
    def registrar_token(self, req: DeviceTokenCreate) -> DeviceTokenResponse:
        model = self.repo.save_token(req.id_usuario, req.fcm_token)
        return DeviceTokenResponse.model_validate(model)
        
    def obtener_token(self, id_usuario: str) -> Optional[str]:
        model = self.repo.get_token(id_usuario)
        return model.fcm_token if model else None

    def enviar_alerta_general(self, req: AlertaCriticidadRequest) -> dict:
        tokens = self.repo.get_all_tokens()
        count = 0
        for t in tokens:
            if t.fcm_token:
                success = firebase_client.send_notification(
                    t.fcm_token,
                    f"¡Alerta de Riesgo {req.nivel_riesgo.upper()}!",
                    req.mensaje
                )
                if success:
                    count += 1
        return {"notificaciones_enviadas": count}
