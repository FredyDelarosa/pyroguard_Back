from abc import ABC, abstractmethod
from typing import List
from domain.model.observacion import ObservacionCampoCreate
from infrastructure.database.postgres.models import ObservacionCampo

class ObservacionRepository(ABC):
    @abstractmethod
    def create(self, observacion_in: ObservacionCampoCreate, id_brigadista: str) -> ObservacionCampo:
        pass

    @abstractmethod
    def get_by_zona(self, id_zona: str) -> List[ObservacionCampo]:
        pass

    @abstractmethod
    def get_by_brigadista(self, id_brigadista: str) -> List[ObservacionCampo]:
        pass
