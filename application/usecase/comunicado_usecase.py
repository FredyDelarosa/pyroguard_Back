from typing import List
from domain.port.comunicado_repository import ComunicadoRepository
from domain.model.comunicado import ComunicadoCreate
from infrastructure.database.postgres.models import Comunicado

class ComunicadoUseCase:
    def __init__(self, repository: ComunicadoRepository):
        self.repository = repository
        
    def obtener_activos(self) -> List[Comunicado]:
        return self.repository.get_activos()
        
    def obtener_todos(self) -> List[Comunicado]:
        return self.repository.get_all()
        
    def crear_comunicado(self, comunicado_in: ComunicadoCreate, id_autor: str) -> Comunicado:
        return self.repository.create(comunicado_in, id_autor)
        
    def borrar_comunicado(self, id_comunicado: str) -> bool:
        return self.repository.delete(id_comunicado)
