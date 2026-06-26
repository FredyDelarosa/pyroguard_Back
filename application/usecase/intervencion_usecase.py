from typing import List, Optional
from domain.port.intervencion_repository import IntervencionRepository
from domain.model.intervencion import IntervencionCreate, IntervencionUpdate
from infrastructure.database.postgres.models import Intervencion

class IntervencionUseCase:
    def __init__(self, repo: IntervencionRepository): self.repo = repo
    def crear(self, intervencion_in: IntervencionCreate) -> Intervencion: return self.repo.create(intervencion_in)
    def actualizar(self, id_intervencion: str, update_data: IntervencionUpdate) -> Optional[Intervencion]: return self.repo.update(id_intervencion, update_data)
    def historial_zona(self, id_zona: str, limit: int = 5) -> List[Intervencion]: return self.repo.get_by_zona(id_zona, limit)
