from abc import ABC, abstractmethod
from typing import List
from features.comunicados.domain.entities import ComunicadoCreate, ComunicadoUpdate
from features.comunicados.infrastructure.models import ComunicadoModel

class ComunicadoRepository(ABC):
    @abstractmethod
    def create(self, comunicado_in: ComunicadoCreate, id_autor: str) -> ComunicadoModel: pass
    @abstractmethod
    def get_all(self) -> List[ComunicadoModel]: pass
    @abstractmethod
    def get_by_id(self, id_comunicado: str) -> ComunicadoModel: pass
    @abstractmethod
    def update(self, id_comunicado: str, comunicado_in: ComunicadoUpdate) -> ComunicadoModel: pass
    @abstractmethod
    def delete(self, id_comunicado: str) -> bool: pass