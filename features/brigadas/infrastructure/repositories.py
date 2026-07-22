from sqlalchemy.orm import Session
from typing import List
from features.brigadas.domain.ports import BrigadaRepository
from features.brigadas.domain.entities import BrigadaCreate
from features.brigadas.infrastructure.models import BrigadaModel, BrigadistaBrigadaModel

class BrigadaRepositoryImpl(BrigadaRepository):
    def __init__(self, db: Session):
        self.db = db
        
    def create(self, brigada_in: BrigadaCreate) -> BrigadaModel:
        nueva_brigada = BrigadaModel(
            nombre=brigada_in.nombre,
            id_coordinador=brigada_in.id_coordinador
        )
        self.db.add(nueva_brigada)
        self.db.commit()
        self.db.refresh(nueva_brigada)
        return nueva_brigada
        
    def get_all(self) -> List[BrigadaModel]:
        return self.db.query(BrigadaModel).order_by(BrigadaModel.creado_en.desc()).all()
        
    def get_by_id(self, id_brigada: str) -> BrigadaModel:
        return self.db.query(BrigadaModel).filter(BrigadaModel.id_brigada == id_brigada).first()
        
    def assign_member(self, id_brigada: str, id_brigadista: str) -> bool:
        brigada = self.db.query(BrigadaModel).filter(BrigadaModel.id_brigada == id_brigada).first()
        
        if not brigada:
            return False
            
        # Verificar si ya está asignado
        existente = self.db.query(BrigadistaBrigadaModel).filter(
            BrigadistaBrigadaModel.id_brigada == id_brigada,
            BrigadistaBrigadaModel.id_usuario == id_brigadista
        ).first()
        
        if existente:
            return True
            
        nueva_relacion = BrigadistaBrigadaModel(
            id_brigada=id_brigada,
            id_usuario=id_brigadista
        )
        self.db.add(nueva_relacion)
        self.db.commit()
        return True
