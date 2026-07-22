from typing import List
from features.comunicados.domain.ports import ComunicadoRepository
from features.comunicados.domain.entities import ComunicadoCreate, ComunicadoResponse
from features.comunicados.infrastructure.models import ComunicadoModel
from core.clients.implementations.auth_service_client import auth_client

class ComunicadoUseCase:
    def __init__(self, repo: ComunicadoRepository): self.repo = repo
    def crear(self, comunicado_in: ComunicadoCreate, id_autor: str) -> ComunicadoResponse: 
        m = self.repo.create(comunicado_in, id_autor)
        return self._build(m)
    def listar(self) -> List[ComunicadoResponse]:
        return [self._build(m) for m in self.repo.get_all()]
    def _build(self, m: ComunicadoModel) -> ComunicadoResponse:
        nombre = None
        if m.id_autor:
            try: 
                info = auth_client.get_user_info(m.id_autor)
                if info: nombre = info.get("nombre")
            except: pass
        return ComunicadoResponse(id_comunicado=str(m.id_comunicado), titulo=m.titulo, contenido=m.contenido, id_autor=str(m.id_autor) if m.id_autor else None, autor_nombre=nombre, fecha_publicacion=m.fecha_publicacion, fecha_vigencia=m.fecha_vigencia)