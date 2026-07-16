from typing import List
from features.observaciones.domain.ports import ObservacionRepository
from features.observaciones.domain.entities import ObservacionCampoCreate, ObservacionCampoResponse
from features.observaciones.infrastructure.models import ObservacionCampoModel
from core.clients.implementations.auth_service_client import auth_client

class ObservacionUseCase:
    def __init__(self, repo: ObservacionRepository): self.repo = repo
    def crear(self, o: ObservacionCampoCreate, id_brigadista: str) -> ObservacionCampoResponse: 
        m = self.repo.create(o, id_brigadista)
        return self._build(m)
    def listar_por_zona(self, id_zona: str) -> List[ObservacionCampoResponse]:
        return [self._build(m) for m in self.repo.get_by_zona(id_zona)]
    def _build(self, m: ObservacionCampoModel) -> ObservacionCampoResponse:
        nombre = None
        if m.id_brigadista:
            try:
                info = auth_client.get_user_info(m.id_brigadista)
                if info: nombre = info.get("nombre")
            except: pass
        return ObservacionCampoResponse(id_observacion=m.id_observacion, id_brigadista=m.id_brigadista, brigadista_nombre=nombre, id_zona=m.id_zona, latitud=m.latitud, longitud=m.longitud, condiciones=m.condiciones, recursos_necesarios=m.recursos_necesarios, observaciones_texto=m.observaciones_texto, creado_en=m.creado_en)