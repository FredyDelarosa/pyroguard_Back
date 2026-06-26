from sqlalchemy.orm import Session
from typing import List
from domain.port.brigada_repository import BrigadaRepository
from domain.model.brigada import BrigadaCreate
from infrastructure.database.postgres.models import Brigada, Usuario, brigadistas_brigada

class BrigadaRepositoryImpl(BrigadaRepository):
    def __init__(self, db: Session):
        self.db = db
        
    def create(self, brigada_in: BrigadaCreate) -> Brigada:
        nueva_brigada = Brigada(
            nombre=brigada_in.nombre,
            id_coordinador=str(brigada_in.id_coordinador) if brigada_in.id_coordinador else None
        )
        self.db.add(nueva_brigada)
        self.db.commit()
        self.db.refresh(nueva_brigada)
        return nueva_brigada
        
    def get_all(self) -> List[Brigada]:
        return self.db.query(Brigada).order_by(Brigada.creado_en.desc()).all()
        
    def assign_member(self, id_brigada: str, id_brigadista: str) -> bool:
        brigada = self.db.query(Brigada).filter(Brigada.id_brigada == id_brigada).first()
        brigadista = self.db.query(Usuario).filter(Usuario.id_usuario == id_brigadista, Usuario.rol == "Brigadista").first()
        
        if not brigada or not brigadista:
            return False
            
        # Verificar si ya está asignado
        if brigadista in brigada.brigadistas:
            return True
            
        brigada.brigadistas.append(brigadista)
        self.db.commit()
        return True
