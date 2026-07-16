from sqlalchemy.orm import Session
from typing import List
from features.reportes_tecnicos.domain.ports import ReporteTecnicoRepository
from features.reportes_tecnicos.domain.entities import ReporteTecnicoCreate
from features.reportes_tecnicos.infrastructure.models import ReporteTecnicoModel

class ReporteTecnicoRepositoryImpl(ReporteTecnicoRepository):
    def __init__(self, db: Session): self.db = db
    def create(self, r: ReporteTecnicoCreate, id_coord: str, pdf: str) -> ReporteTecnicoModel:
        nuevo = ReporteTecnicoModel(id_zona=str(r.id_zona), id_coordinador=id_coord, nivel_riesgo_registrado=r.nivel_riesgo_registrado, archivo_pdf_path=pdf)
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)
        return nuevo
    def get_by_zona(self, id_zona: str) -> List[ReporteTecnicoModel]:
        return self.db.query(ReporteTecnicoModel).filter(ReporteTecnicoModel.id_zona == id_zona).order_by(ReporteTecnicoModel.creado_en.desc()).all()