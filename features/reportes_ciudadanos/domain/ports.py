from abc import ABC, abstractmethod
from typing import List
from features.reportes_ciudadanos.domain.entities import ReporteCiudadanoCreate
from features.reportes_ciudadanos.infrastructure.models import ReporteCiudadanoModel

class ReporteCiudadanoRepository(ABC):
    @abstractmethod
    def create(self, reporte_in: ReporteCiudadanoCreate) -> ReporteCiudadanoModel:
        pass
    @abstractmethod
    def get_all(self) -> List[ReporteCiudadanoModel]:
        pass
    @abstractmethod
    def update_estado(self, id_reporte: str, estado: str) -> ReporteCiudadanoModel:
        pass
