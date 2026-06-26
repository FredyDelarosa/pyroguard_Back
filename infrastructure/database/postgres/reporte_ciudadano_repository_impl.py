from sqlalchemy.orm import Session
from typing import List
from domain.port.reporte_ciudadano_repository import ReporteCiudadanoRepository
from domain.model.reporte import ReporteCiudadanoCreate
from infrastructure.database.postgres.models import ReporteCiudadano

class ReporteCiudadanoRepositoryImpl(ReporteCiudadanoRepository):
    def __init__(self, db: Session): self.db = db
    def create(self, reporte_in: ReporteCiudadanoCreate) -> ReporteCiudadano:
        nuevo = ReporteCiudadano(descripcion=reporte_in.descripcion, id_zona=reporte_in.id_zona, foto_url=reporte_in.foto_url, anonimo=reporte_in.anonimo)
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)
        return nuevo
    def get_all(self) -> List[ReporteCiudadano]:
        return self.db.query(ReporteCiudadano).order_by(ReporteCiudadano.creado_en.desc()).all()
