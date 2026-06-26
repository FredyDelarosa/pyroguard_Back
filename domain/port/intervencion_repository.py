from abc import ABC, abstractmethod
from typing import List, Optional
from domain.model.intervencion import IntervencionCreate, IntervencionUpdate
from infrastructure.database.postgres.models import Intervencion

class IntervencionRepository(ABC):
    @abstractmethod
    def create(self, intervencion_in: IntervencionCreate) -> Intervencion: pass
    @abstractmethod
    def update(self, id_intervencion: str, update_data: IntervencionUpdate) -> Optional[Intervencion]: pass
    @abstractmethod
    def get_by_zona(self, id_zona: str, limit: int) -> List[Intervencion]: pass
