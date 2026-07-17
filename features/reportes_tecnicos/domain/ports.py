from abc import ABC, abstractmethod
from typing import List, Optional
from features.reportes_tecnicos.infrastructure.models import ReporteTecnicoModel

class ReporteTecnicoRepository(ABC):
    @abstractmethod
    def create_pending(self, id_zona: str, id_coord: str, task_id: str) -> ReporteTecnicoModel: pass
    @abstractmethod
    def update_completed(self, task_id: str, pdf_path: str, nivel_riesgo: str) -> Optional[ReporteTecnicoModel]: pass
    @abstractmethod
    def get_by_zona(self, id_zona: str) -> List[ReporteTecnicoModel]: pass