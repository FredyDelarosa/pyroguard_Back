from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import List, Optional
from domain.port.comunicado_repository import ComunicadoRepository
from domain.model.comunicado import ComunicadoCreate
from infrastructure.database.postgres.models import Comunicado

class ComunicadoRepositoryImpl(ComunicadoRepository):
    def __init__(self, db: Session):
        self.db = db
        
    def get_activos(self) -> List[Comunicado]:
        return self.db.query(Comunicado).filter(Comunicado.fecha_vigencia > func.now()).order_by(Comunicado.creado_en.desc()).all()
        
    def get_all(self) -> List[Comunicado]:
        return self.db.query(Comunicado).order_by(Comunicado.creado_en.desc()).all()
        
    def create(self, comunicado_in: ComunicadoCreate, id_autor: str) -> Comunicado:
        nuevo_comunicado = Comunicado(
            titulo=comunicado_in.titulo,
            contenido=comunicado_in.contenido,
            zonas_aplica=",".join(comunicado_in.zonas_aplica) if comunicado_in.zonas_aplica else "Todas",
            fecha_vigencia=comunicado_in.fecha_vigencia,
            id_autor=id_autor
        )
        self.db.add(nuevo_comunicado)
        self.db.commit()
        self.db.refresh(nuevo_comunicado)
        return nuevo_comunicado
        
    def delete(self, id_comunicado: str) -> bool:
        comunicado = self.db.query(Comunicado).filter(Comunicado.id_comunicado == id_comunicado).first()
        if not comunicado:
            return False
            
        self.db.delete(comunicado)
        self.db.commit()
        return True
