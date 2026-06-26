from typing import List, Optional
from domain.port.reporte_tecnico_repository import ReporteTecnicoRepository
from domain.model.reporte import ReporteTecnicoCreate
from infrastructure.database.postgres.models import ReporteTecnico
from core.utils.pdf_generator import generate_technical_report

class ReporteTecnicoUseCase:
    def __init__(self, repo: ReporteTecnicoRepository): self.repo = repo
    def generar(self, reporte_in: ReporteTecnicoCreate, id_coordinador: str, coordinador_nombre: str) -> ReporteTecnico:
        pdf_path = generate_technical_report(id_zona=str(reporte_in.id_zona), nivel_riesgo=reporte_in.nivel_riesgo_registrado, coordinador_nombre=coordinador_nombre)
        return self.repo.create(reporte_in, id_coordinador, pdf_path)
    def listar(self) -> List[ReporteTecnico]: return self.repo.get_all()
    def obtener_archivo(self, id_reporte: str) -> Optional[str]:
        rep = self.repo.get_by_id(id_reporte)
        return rep.archivo_pdf_path if rep else None
