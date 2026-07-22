from abc import ABC, abstractmethod
from typing import List, Optional
from features.brigadas.domain.entities import BrigadaCreate
from features.brigadas.infrastructure.models import BrigadaModel

class BrigadaRepository(ABC):
    @abstractmethod
    def create(self, brigada_in: BrigadaCreate) -> BrigadaModel:
        pass

    @abstractmethod
    def get_all(self) -> List[BrigadaModel]:
        pass

    @abstractmethod
    def get_by_id(self, id_brigada: str) -> Optional[BrigadaModel]:
        pass

    @abstractmethod
    def assign_member(self, id_brigada: str, id_brigadista: str) -> bool:
        pass
