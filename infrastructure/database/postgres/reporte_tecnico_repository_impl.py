from sqlalchemy.orm import Session
from typing import List, Optional
from domain.port.reporte_tecnico_repository import ReporteTecnicoRepository
from domain.model.reporte import ReporteTecnicoCreate
from infrastructure.database.postgres.models import ReporteTecnico

class ReporteTecnicoRepositoryImpl(ReporteTecnicoRepository):
    def __init__(self, db: Session): self.db = db
    def create(self, reporte_in: ReporteTecnicoCreate, id_coordinador: str, pdf_path: str) -> ReporteTecnico:
        nuevo = ReporteTecnico(id_zona=reporte_in.id_zona, id_coordinador=id_coordinador, nivel_riesgo_registrado=reporte_in.nivel_riesgo_registrado, archivo_pdf_path=pdf_path)
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)
        return nuevo
    def get_all(self) -> List[ReporteTecnico]: return self.db.query(ReporteTecnico).order_by(ReporteTecnico.creado_en.desc()).all()
    def get_by_id(self, id_reporte: str) -> Optional[ReporteTecnico]: return self.db.query(ReporteTecnico).filter(ReporteTecnico.id_reporte == id_reporte).first()
