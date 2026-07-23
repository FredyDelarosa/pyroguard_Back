from typing import List
from features.intervenciones.domain.ports import IntervencionRepository
from features.intervenciones.domain.entities import IntervencionCreate, IntervencionUpdate, IntervencionResponse
from features.brigadas.domain.ports import BrigadaRepository
from features.notificaciones.domain.ports import DeviceTokenRepository
from core.clients.implementations.firebase_client import firebase_client

class IntervencionUseCase:
    def __init__(
        self, 
        repo: IntervencionRepository,
        brigada_repo: BrigadaRepository = None,
        token_repo: DeviceTokenRepository = None
    ): 
        self.repo = repo
        self.brigada_repo = brigada_repo
        self.token_repo = token_repo
        
    def crear(self, i: IntervencionCreate) -> IntervencionResponse: 
        intervencion_model = self.repo.create(i)
        
        # Enviar notificación a brigadistas
        if self.brigada_repo and self.token_repo:
            brigada = self.brigada_repo.get_by_id(str(i.id_brigada))
            if brigada:
                # Extraemos brigadistas (de la relación)
                for rel in getattr(brigada, 'brigadistas_rel', []):
                    token_model = self.token_repo.get_token(str(rel.id_usuario))
                    if token_model and token_model.fcm_token:
                        firebase_client.send_notification(
                            token_model.fcm_token,
                            "Nueva Intervención Asignada",
                            f"Se ha asignado una nueva intervención a tu brigada ({brigada.nombre})."
                        )
                        
        return IntervencionResponse.model_validate(intervencion_model)
        
    def actualizar(self, id: str, i: IntervencionUpdate) -> IntervencionResponse: 
        m = self.repo.update(id, i)
        if not m:
            return None
            
        # Si se finaliza o completa, notificar al coordinador
        if i.estado in ["Completada", "Finalizada"] and self.brigada_repo and self.token_repo:
            brigada = self.brigada_repo.get_by_id(str(m.id_brigada))
            if brigada and brigada.id_coordinador:
                token_model = self.token_repo.get_token(str(brigada.id_coordinador))
                if token_model and token_model.fcm_token:
                    firebase_client.send_notification(
                        token_model.fcm_token,
                        "Intervención Completada",
                        f"La brigada {brigada.nombre} ha completado la intervención."
                    )
                    
        return IntervencionResponse.model_validate(m)
        
    def historial_zona(self, id_zona: str, limit: int) -> List[IntervencionResponse]: 
        return [IntervencionResponse.model_validate(m) for m in self.repo.get_by_zona(id_zona, limit)]
        
    def listar_mis_tareas(self, id_usuario: str) -> List[IntervencionResponse]:
        # Devuelve las intervenciones que no están completadas para el brigadista
        return [IntervencionResponse.model_validate(m) for m in self.repo.get_by_brigadista(id_usuario)]