from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import List, Optional
from domain.port.intervencion_repository import IntervencionRepository
from domain.model.intervencion import IntervencionCreate, IntervencionUpdate
from infrastructure.database.postgres.models import Intervencion

class IntervencionRepositoryImpl(IntervencionRepository):
    def __init__(self, db: Session): self.db = db
    def create(self, intervencion_in: IntervencionCreate, id_brigada: str) -> Intervencion:
        nueva = Intervencion(
            id_zona=intervencion_in.id_zona,
            id_brigada=id_brigada,
            estrategia_asignada=intervencion_in.estrategia_asignada
        )
        self.db.add(nueva)
        self.db.commit()
        self.db.refresh(nueva)
        return nueva
    def update(self, id_intervencion: str, update_data: IntervencionUpdate) -> Optional[Intervencion]:
        intervencion = self.db.query(Intervencion).filter(Intervencion.id_intervencion == id_intervencion).first()
        if not intervencion: return None
        if update_data.estado is not None: intervencion.estado = update_data.estado
        if update_data.observaciones is not None: intervencion.observaciones = update_data.observaciones
        if update_data.estado in ["Completada", "Cancelada"]: intervencion.fecha_completada = func.now()
        self.db.commit()
        self.db.refresh(intervencion)
        return intervencion
    def get_by_zona(self, id_zona: str, limit: int) -> List[Intervencion]:
        return self.db.query(Intervencion).filter(Intervencion.id_zona == id_zona).order_by(Intervencion.fecha_asignacion.desc()).limit(limit).all()
