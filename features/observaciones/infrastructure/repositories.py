from sqlalchemy.orm import Session
from typing import List
from features.observaciones.domain.ports import ObservacionRepository
from features.observaciones.domain.entities import ObservacionCampoCreate
from features.observaciones.infrastructure.models import ObservacionCampoModel

class ObservacionRepositoryImpl(ObservacionRepository):
    def __init__(self, db: Session): self.db = db
    def create(self, o: ObservacionCampoCreate, id_brigadista: str) -> ObservacionCampoModel:
        nuevo = ObservacionCampoModel(id_brigadista=id_brigadista, id_zona=str(o.id_zona), latitud=o.latitud, longitud=o.longitud, condiciones=o.condiciones, recursos_necesarios=o.recursos_necesarios, observaciones_texto=o.observaciones_texto)
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)
        return nuevo
    def get_by_zona(self, id_zona: str) -> List[ObservacionCampoModel]:
        return self.db.query(ObservacionCampoModel).filter(ObservacionCampoModel.id_zona == id_zona).order_by(ObservacionCampoModel.creado_en.desc()).all()