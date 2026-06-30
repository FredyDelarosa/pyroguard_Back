from sqlalchemy.orm import Session
from typing import List
from domain.port.reporte_ciudadano_repository import ReporteCiudadanoRepository
from domain.model.reporte import ReporteCiudadanoCreate
from infrastructure.database.postgres.models import ReporteCiudadano
from core.security import persistence_interceptor

class ReporteCiudadanoRepositoryImpl(ReporteCiudadanoRepository):
    def __init__(self, db: Session): self.db = db
    def create(self, reporte_in: ReporteCiudadanoCreate) -> ReporteCiudadano:
        nuevo = ReporteCiudadano(
            descripcion=reporte_in.descripcion,
            latitud=reporte_in.latitud,
            longitud=reporte_in.longitud,
            foto_url=reporte_in.foto_url
        )
        nuevo = persistence_interceptor.prepare_for_write(nuevo)
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)
        return persistence_interceptor.materialize_from_read(nuevo)
    def get_all(self) -> List[ReporteCiudadano]:
        reportes = self.db.query(ReporteCiudadano).order_by(ReporteCiudadano.creado_en.desc()).all()
        return [persistence_interceptor.materialize_from_read(r) for r in reportes]
    def update_estado(self, id_reporte: str, nuevo_estado: str) -> ReporteCiudadano:
        reporte = self.db.query(ReporteCiudadano).filter(ReporteCiudadano.id_reporte == id_reporte).first()
        if reporte:
            reporte.estado = nuevo_estado
            reporte = persistence_interceptor.prepare_for_write(reporte)
            self.db.commit()
            self.db.refresh(reporte)
            reporte = persistence_interceptor.materialize_from_read(reporte)
        return reporte
