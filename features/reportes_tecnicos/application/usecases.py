from typing import List
from features.reportes_tecnicos.domain.ports import ReporteTecnicoRepository
from features.reportes_tecnicos.domain.entities import ReporteTecnicoCreate, ReporteTecnicoResponse
from features.reportes_tecnicos.infrastructure.models import ReporteTecnicoModel
from core.clients.implementations.auth_service_client import auth_client

class ReporteTecnicoUseCase:
    def __init__(self, repo: ReporteTecnicoRepository): self.repo = repo
    def generar(self, r: ReporteTecnicoCreate, id_coord: str) -> ReporteTecnicoResponse:
        # Generacion stub PDF
        pdf_path = f"/app/storage/reportes/reporte_{r.id_zona}.pdf"
        m = self.repo.create(r, id_coord, pdf_path)
        return self._build(m)
    def listar(self, id_zona: str) -> List[ReporteTecnicoResponse]:
        return [self._build(m) for m in self.repo.get_by_zona(id_zona)]
    def _build(self, m: ReporteTecnicoModel) -> ReporteTecnicoResponse:
        nombre = None
        if m.id_coordinador:
            try:
                info = auth_client.get_user_info(m.id_coordinador)
                if info: nombre = info.get("nombre")
            except: pass
        return ReporteTecnicoResponse(id_reporte=m.id_reporte, id_zona=m.id_zona, id_coordinador=m.id_coordinador, coordinador_nombre=nombre, nivel_riesgo_registrado=m.nivel_riesgo_registrado, archivo_pdf_path=m.archivo_pdf_path, creado_en=m.creado_en)