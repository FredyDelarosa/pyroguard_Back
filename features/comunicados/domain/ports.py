from abc import ABC, abstractmethod
from typing import List
from features.comunicados.domain.entities import ComunicadoCreate
from features.comunicados.infrastructure.models import ComunicadoModel

class ComunicadoRepository(ABC):
    @abstractmethod
    def create(self, comunicado_in: ComunicadoCreate, id_autor: str) -> ComunicadoModel: pass
    @abstractmethod
    def get_all(self) -> List[ComunicadoModel]: pass