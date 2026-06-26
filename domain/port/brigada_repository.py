from abc import ABC, abstractmethod
from typing import List, Optional
from domain.model.brigada import BrigadaCreate
from infrastructure.database.postgres.models import Brigada

class BrigadaRepository(ABC):
    @abstractmethod
    def create(self, brigada_in: BrigadaCreate) -> Brigada:
        pass

    @abstractmethod
    def get_all(self) -> List[Brigada]:
        pass

    @abstractmethod
    def assign_member(self, id_brigada: str, id_brigadista: str) -> bool:
        pass
