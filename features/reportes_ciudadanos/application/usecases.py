from typing import List
from features.reportes_ciudadanos.domain.ports import ReporteCiudadanoRepository
from features.reportes_ciudadanos.domain.entities import ReporteCiudadanoCreate
from features.reportes_ciudadanos.infrastructure.models import ReporteCiudadanoModel

class ReporteCiudadanoUseCase:
    def __init__(self, repo: ReporteCiudadanoRepository): 
        self.repo = repo
        
    def crear(self, reporte_in: ReporteCiudadanoCreate) -> ReporteCiudadanoModel: 
        return self.repo.create(reporte_in)
        
    def listar(self) -> List[ReporteCiudadanoModel]: 
        return self.repo.get_all()
        
    def update_estado(self, id_reporte: str, estado: str) -> ReporteCiudadanoModel: 
        return self.repo.update_estado(id_reporte, estado)
