from abc import ABC, abstractmethod
from typing import List, Optional
from domain.model.usuario import UsuarioCreate, UsuarioUpdate
from infrastructure.database.postgres.models import Usuario

class UsuarioRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Usuario]:
        pass
        
    @abstractmethod
    def get_by_id(self, id_usuario: str) -> Optional[Usuario]:
        pass
        
    @abstractmethod
    def update(self, id_usuario: str, update_data: UsuarioUpdate) -> Optional[Usuario]:
        pass
        
    @abstractmethod
    def delete(self, id_usuario: str) -> bool:
        pass
