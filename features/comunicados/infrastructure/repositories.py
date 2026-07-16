from sqlalchemy.orm import Session
from typing import List
from features.comunicados.domain.ports import ComunicadoRepository
from features.comunicados.domain.entities import ComunicadoCreate
from features.comunicados.infrastructure.models import ComunicadoModel

class ComunicadoRepositoryImpl(ComunicadoRepository):
    def __init__(self, db: Session): self.db = db
    def create(self, comunicado_in: ComunicadoCreate, id_autor: str) -> ComunicadoModel:
        nuevo = ComunicadoModel(titulo=comunicado_in.titulo, contenido=comunicado_in.contenido, fecha_vigencia=comunicado_in.fecha_vigencia, id_autor=id_autor)
        self.db.add(nuevo)
        self.db.commit()
        self.db.refresh(nuevo)
        return nuevo
    def get_all(self) -> List[ComunicadoModel]:
        return self.db.query(ComunicadoModel).order_by(ComunicadoModel.fecha_publicacion.desc()).all()