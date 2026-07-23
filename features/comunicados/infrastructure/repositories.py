from sqlalchemy.orm import Session
from typing import List
from features.comunicados.domain.ports import ComunicadoRepository
from features.comunicados.domain.entities import ComunicadoCreate, ComunicadoUpdate
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
    
    def get_by_id(self, id_comunicado: str) -> ComunicadoModel:
        return self.db.query(ComunicadoModel).filter(ComunicadoModel.id_comunicado == id_comunicado).first()

    def update(self, id_comunicado: str, comunicado_in: ComunicadoUpdate) -> ComunicadoModel:
        comunicado = self.get_by_id(id_comunicado)
        if not comunicado:
            return None
        if comunicado_in.titulo is not None:
            comunicado.titulo = comunicado_in.titulo
        if comunicado_in.contenido is not None:
            comunicado.contenido = comunicado_in.contenido
        if comunicado_in.fecha_vigencia is not None:
            comunicado.fecha_vigencia = comunicado_in.fecha_vigencia
        self.db.commit()
        self.db.refresh(comunicado)
        return comunicado

    def delete(self, id_comunicado: str) -> bool:
        comunicado = self.get_by_id(id_comunicado)
        if not comunicado:
            return False
        self.db.delete(comunicado)
        self.db.commit()
        return True