from abc import ABC, abstractmethod
from typing import List
from features.reportes_tecnicos.domain.entities import ReporteTecnicoCreate
from features.reportes_tecnicos.infrastructure.models import ReporteTecnicoModel

class ReporteTecnicoRepository(ABC):
    @abstractmethod
    def create(self, r: ReporteTecnicoCreate, id_coord: str, pdf: str) -> ReporteTecnicoModel: pass
    @abstractmethod
    def get_by_zona(self, id_zona: str) -> List[ReporteTecnicoModel]: pass