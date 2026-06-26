from typing import List
from domain.port.reporte_ciudadano_repository import ReporteCiudadanoRepository
from domain.model.reporte import ReporteCiudadanoCreate
from infrastructure.database.postgres.models import ReporteCiudadano

class ReporteCiudadanoUseCase:
    def __init__(self, repo: ReporteCiudadanoRepository): self.repo = repo
    def crear(self, reporte_in: ReporteCiudadanoCreate) -> ReporteCiudadano: return self.repo.create(reporte_in)
    def listar(self) -> List[ReporteCiudadano]: return self.repo.get_all()
    def update_estado(self, id_reporte: str, estado: str) -> ReporteCiudadano: return self.repo.update_estado(id_reporte, estado)
