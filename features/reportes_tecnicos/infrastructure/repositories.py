from sqlalchemy.orm import Session
from typing import List, Optional
from features.reportes_tecnicos.domain.ports import ReporteTecnicoRepository
from features.reportes_tecnicos.infrastructure.models import ReporteTecnicoModel

class ReporteTecnicoRepositoryImpl(ReporteTecnicoRepository):
    def __init__(self, db: Session): 
        self.db = db

    def create_pending(self, id_zona: str, id_coord: str, task_id: str) -> ReporteTecnicoModel:
        nuevo = ReporteTecnicoModel(
            id_zona=id_zona, 
            id_coordinador=id_coord, 
            task_id=task_id, 
            estado="PROCESANDO"
        )
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)
        return nuevo
    
    def update_completed(self, task_id: str, pdf_path: str, nivel_riesgo: str) -> Optional[ReporteTecnicoModel]:
        reporte = self.db.query(ReporteTecnicoModel).filter(ReporteTecnicoModel.task_id == task_id).first()
        if reporte:
            reporte.estado = "COMPLETADO"
            reporte.archivo_pdf_path = pdf_path
            reporte.nivel_riesgo_registrado = nivel_riesgo
            self.db.commit()
            self.db.refresh(reporte)
        return reporte
        
    def get_by_zona(self, id_zona: str) -> List[ReporteTecnicoModel]:
        return self.db.query(ReporteTecnicoModel).filter(ReporteTecnicoModel.id_zona == id_zona).order_by(ReporteTecnicoModel.creado_en.desc()).all()