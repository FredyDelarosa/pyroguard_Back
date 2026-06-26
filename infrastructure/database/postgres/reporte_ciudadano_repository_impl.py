from sqlalchemy.orm import Session
from typing import List
from domain.port.reporte_ciudadano_repository import ReporteCiudadanoRepository
from domain.model.reporte import ReporteCiudadanoCreate
from infrastructure.database.postgres.models import ReporteCiudadano

class ReporteCiudadanoRepositoryImpl(ReporteCiudadanoRepository):
    def __init__(self, db: Session): self.db = db
    def create(self, reporte_in: ReporteCiudadanoCreate) -> ReporteCiudadano:
        nuevo = ReporteCiudadano(
            descripcion=reporte_in.descripcion,
            latitud=reporte_in.latitud,
            longitud=reporte_in.longitud,
            foto_url=reporte_in.foto_url
        )
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)
        return nuevo
    def get_all(self) -> List[ReporteCiudadano]:
        return self.db.query(ReporteCiudadano).order_by(ReporteCiudadano.creado_en.desc()).all()
    def update_estado(self, id_reporte: str, nuevo_estado: str) -> ReporteCiudadano:
        reporte = self.db.query(ReporteCiudadano).filter(ReporteCiudadano.id_reporte == id_reporte).first()
        if reporte:
            reporte.estado = nuevo_estado
            self.db.commit()
            self.db.refresh(reporte)
        return reporte
