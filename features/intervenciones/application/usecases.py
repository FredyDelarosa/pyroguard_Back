from typing import List
from features.intervenciones.domain.ports import IntervencionRepository
from features.intervenciones.domain.entities import IntervencionCreate, IntervencionUpdate, IntervencionResponse

class IntervencionUseCase:
    def __init__(self, repo: IntervencionRepository): self.repo = repo
    def crear(self, i: IntervencionCreate) -> IntervencionResponse: return IntervencionResponse.model_validate(self.repo.create(i))
    def actualizar(self, id: str, i: IntervencionUpdate) -> IntervencionResponse: 
        m = self.repo.update(id, i)
        return IntervencionResponse.model_validate(m) if m else None
    def historial_zona(self, id_zona: str, limit: int) -> List[IntervencionResponse]: return [IntervencionResponse.model_validate(m) for m in self.repo.get_by_zona(id_zona, limit)]