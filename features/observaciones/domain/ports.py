from abc import ABC, abstractmethod
from typing import List
from features.observaciones.domain.entities import ObservacionCampoCreate
from features.observaciones.infrastructure.models import ObservacionCampoModel

class ObservacionRepository(ABC):
    @abstractmethod
    def create(self, o: ObservacionCampoCreate, id_brigadista: str) -> ObservacionCampoModel: pass
    @abstractmethod
    def get_by_zona(self, id_zona: str) -> List[ObservacionCampoModel]: pass