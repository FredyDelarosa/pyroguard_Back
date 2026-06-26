from abc import ABC, abstractmethod
from typing import List, Optional
from domain.model.comunicado import ComunicadoCreate
from infrastructure.database.postgres.models import Comunicado

class ComunicadoRepository(ABC):
    @abstractmethod
    def get_activos(self) -> List[Comunicado]:
        pass
        
    @abstractmethod
    def get_all(self) -> List[Comunicado]:
        pass
        
    @abstractmethod
    def create(self, comunicado_in: ComunicadoCreate, id_autor: str) -> Comunicado:
        pass
        
    @abstractmethod
    def delete(self, id_comunicado: str) -> bool:
        pass
