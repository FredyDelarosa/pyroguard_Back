from typing import List
from features.brigadas.domain.ports import BrigadaRepository
from features.brigadas.domain.entities import BrigadaCreate, BrigadaResponse
from core.clients.implementations.auth_service_client import auth_client

class BrigadaUseCase:
    def __init__(self, repository: BrigadaRepository):
        self.repository = repository
        
    def crear_brigada(self, brigada_in: BrigadaCreate) -> BrigadaResponse:
        # Validar si el coordinador existe
        if brigada_in.id_coordinador:
            user_info = auth_client.get_user_info(str(brigada_in.id_coordinador))
            if not user_info or "Coordinador" not in user_info.get("roles", []):
                raise ValueError("El coordinador no existe o no tiene el rol adecuado.")
                
        model = self.repository.create(brigada_in)
        return self._build_response(model)
        
    def listar_brigadas(self) -> List[BrigadaResponse]:
        models = self.repository.get_all()
        return [self._build_response(m) for m in models]
        
    def asignar_brigadista(self, id_brigada: str, id_brigadista: str) -> bool:
        # Comunicarse con el microservicio Auth para asegurar que el ID es un Brigadista válido
        user_info = auth_client.get_user_info(id_brigadista)
        if not user_info or "Brigadista" not in user_info.get("roles", []):
            raise ValueError("El usuario no existe o no tiene el rol de Brigadista.")
            
        success = self.repository.assign_member(id_brigada, id_brigadista)
        if not success:
            raise ValueError("La brigada no existe.")
        return True

    def _build_response(self, model) -> BrigadaResponse:
        coordinador_nombre = None
        if model.id_coordinador:
            try:
                user_info = auth_client.get_user_info(model.id_coordinador)
                if user_info:
                    coordinador_nombre = user_info.get("nombre")
            except Exception:
                pass
                
        brigadistas_ids = [rel.id_usuario for rel in getattr(model, 'brigadistas_rel', [])]
                
        return BrigadaResponse(
            id_brigada=model.id_brigada,
            nombre=model.nombre,
            id_coordinador=model.id_coordinador,
            coordinador_nombre=coordinador_nombre,
            activa=model.activa,
            creado_en=model.creado_en,
            brigadistas=brigadistas_ids
        )
