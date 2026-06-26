from sqlalchemy.orm import Session
from typing import List
from domain.port.observacion_repository import ObservacionRepository
from domain.model.observacion import ObservacionCampoCreate
from infrastructure.database.postgres.models import ObservacionCampo

class ObservacionRepositoryImpl(ObservacionRepository):
    def __init__(self, db: Session):
        self.db = db
        
    def create(self, observacion_in: ObservacionCampoCreate, id_brigadista: str) -> ObservacionCampo:
        nueva_obs = ObservacionCampo(
            id_brigadista=id_brigadista,
            id_zona=observacion_in.id_zona,
            latitud=observacion_in.latitud,
            longitud=observacion_in.longitud,
            condiciones=observacion_in.condiciones,
            recursos_necesarios=observacion_in.recursos_necesarios,
            observaciones_texto=observacion_in.observaciones_texto
        )
        self.db.add(nueva_obs)
        self.db.commit()
        self.db.refresh(nueva_obs)
        return nueva_obs
        
    def get_by_zona(self, id_zona: str) -> List[ObservacionCampo]:
        return self.db.query(ObservacionCampo).filter(ObservacionCampo.id_zona == id_zona).order_by(ObservacionCampo.creado_en.desc()).all()
        
    def get_by_brigadista(self, id_brigadista: str) -> List[ObservacionCampo]:
        return self.db.query(ObservacionCampo).filter(ObservacionCampo.id_brigadista == id_brigadista).order_by(ObservacionCampo.creado_en.desc()).all()
