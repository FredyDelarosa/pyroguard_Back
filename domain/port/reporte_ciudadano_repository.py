from abc import ABC, abstractmethod
from typing import List
from domain.model.reporte import ReporteCiudadanoCreate
from infrastructure.database.postgres.models import ReporteCiudadano

class ReporteCiudadanoRepository(ABC):
    @abstractmethod
    def create(self, reporte_in: ReporteCiudadanoCreate) -> ReporteCiudadano: pass
    @abstractmethod
    def get_all(self) -> List[ReporteCiudadano]: pass
    @abstractmethod
    def update_estado(self, id_reporte: str, nuevo_estado: str) -> ReporteCiudadano: pass
