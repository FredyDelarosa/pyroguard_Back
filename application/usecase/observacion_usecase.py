from typing import List
from domain.port.observacion_repository import ObservacionRepository
from domain.model.observacion import ObservacionCampoCreate
from infrastructure.database.postgres.models import ObservacionCampo

class ObservacionUseCase:
    def __init__(self, repository: ObservacionRepository):
        self.repository = repository
        
    def registrar_observacion(self, observacion_in: ObservacionCampoCreate, id_brigadista: str) -> ObservacionCampo:
        return self.repository.create(observacion_in, id_brigadista)
        
    def listar_por_zona(self, id_zona: str) -> List[ObservacionCampo]:
        return self.repository.get_by_zona(id_zona)
        
    def listar_por_brigadista(self, id_brigadista: str) -> List[ObservacionCampo]:
        return self.repository.get_by_brigadista(id_brigadista)
