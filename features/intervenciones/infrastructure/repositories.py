from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone
from features.intervenciones.domain.ports import IntervencionRepository
from features.intervenciones.domain.entities import IntervencionCreate, IntervencionUpdate
from features.intervenciones.infrastructure.models import IntervencionModel

class IntervencionRepositoryImpl(IntervencionRepository):
    def __init__(self, db: Session): self.db = db
    def create(self, int_in: IntervencionCreate) -> IntervencionModel:
        nuevo = IntervencionModel(id_brigada=str(int_in.id_brigada), id_zona=str(int_in.id_zona), estado=int_in.estado, observaciones=int_in.observaciones)
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)
        return nuevo
    def update(self, id_int: str, int_in: IntervencionUpdate) -> IntervencionModel:
        intervencion = self.db.query(IntervencionModel).filter(IntervencionModel.id_intervencion == id_int).first()
        if intervencion:
            intervencion.estado = int_in.estado
            if int_in.observaciones: intervencion.observaciones = int_in.observaciones
            if int_in.estado == "Completada": intervencion.fecha_completada = datetime.now(timezone.utc)
            self.db.commit()
            self.db.refresh(intervencion)
        return intervencion
    def get_by_zona(self, id_zona: str, limit: int) -> List[IntervencionModel]:
        return self.db.query(IntervencionModel).filter(IntervencionModel.id_zona == id_zona).order_by(IntervencionModel.fecha_asignacion.desc()).limit(limit).all()
        
    def get_by_brigadista(self, id_usuario: str) -> List[IntervencionModel]:
        from features.brigadas.infrastructure.models import BrigadistaBrigadaModel
        return self.db.query(IntervencionModel).join(
            BrigadistaBrigadaModel, 
            IntervencionModel.id_brigada == BrigadistaBrigadaModel.id_brigada
        ).filter(
            BrigadistaBrigadaModel.id_usuario == id_usuario,
            IntervencionModel.estado != "Completada"
        ).order_by(IntervencionModel.fecha_asignacion.desc()).all()