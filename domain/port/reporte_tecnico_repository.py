from abc import ABC, abstractmethod
from typing import List, Optional
from domain.model.reporte import ReporteTecnicoCreate
from infrastructure.database.postgres.models import ReporteTecnico

class ReporteTecnicoRepository(ABC):
    @abstractmethod
    def create(self, reporte_in: ReporteTecnicoCreate, id_coordinador: str, pdf_path: str) -> ReporteTecnico: pass
    @abstractmethod
    def get_all(self) -> List[ReporteTecnico]: pass
    @abstractmethod
    def get_by_id(self, id_reporte: str) -> Optional[ReporteTecnico]: pass
