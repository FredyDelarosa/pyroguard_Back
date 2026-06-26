from typing import List
from domain.port.brigada_repository import BrigadaRepository
from domain.model.brigada import BrigadaCreate
from infrastructure.database.postgres.models import Brigada

class BrigadaUseCase:
    def __init__(self, repository: BrigadaRepository):
        self.repository = repository
        
    def crear_brigada(self, brigada_in: BrigadaCreate) -> Brigada:
        return self.repository.create(brigada_in)
        
    def listar_brigadas(self) -> List[Brigada]:
        return self.repository.get_all()
        
    def asignar_brigadista(self, id_brigada: str, id_brigadista: str) -> bool:
        return self.repository.assign_member(id_brigada, id_brigadista)
