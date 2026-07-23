from abc import ABC, abstractmethod
from typing import List
from features.intervenciones.domain.entities import IntervencionCreate, IntervencionUpdate
from features.intervenciones.infrastructure.models import IntervencionModel

class IntervencionRepository(ABC):
    @abstractmethod
    def create(self, int_in: IntervencionCreate) -> IntervencionModel: pass
    @abstractmethod
    def update(self, id_int: str, int_in: IntervencionUpdate) -> IntervencionModel: pass
    @abstractmethod
    def get_by_zona(self, id_zona: str, limit: int) -> List[IntervencionModel]: pass
    @abstractmethod
    def get_by_brigadista(self, id_usuario: str) -> List[IntervencionModel]: pass