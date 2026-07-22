from typing import List
from features.comunicados.domain.ports import ComunicadoRepository
from features.comunicados.domain.entities import ComunicadoCreate, ComunicadoResponse, EmergenciaCreate
from features.comunicados.infrastructure.models import ComunicadoModel
from core.clients.implementations.auth_service_client import auth_client
from features.notificaciones.domain.ports import DeviceTokenRepository
from core.clients.implementations.firebase_client import firebase_client

class ComunicadoUseCase:
    def __init__(self, repo: ComunicadoRepository, token_repo: DeviceTokenRepository = None): 
        self.repo = repo
        self.token_repo = token_repo
        
    def crear(self, comunicado_in: ComunicadoCreate, id_autor: str) -> ComunicadoResponse: 
        m = self.repo.create(comunicado_in, id_autor)
        return self._build(m)
        
    def declarar_emergencia(self, emergencia_in: EmergenciaCreate, id_autor: str) -> ComunicadoResponse:
        # 1. Crear comunicado oficial
        titulo = "🚨 ESTADO DE EMERGENCIA DECLARADO"
        contenido = f"La zona {emergencia_in.id_zona} está bajo riesgo inminente."
        if emergencia_in.mensaje_adicional:
            contenido += f" Instrucciones: {emergencia_in.mensaje_adicional}"
            
        comunicado_create = ComunicadoCreate(
            titulo=titulo,
            contenido=contenido,
            fecha_vigencia=emergencia_in.fecha_vigencia
        )
        
        m = self.repo.create(comunicado_create, id_autor)
        
        # 2. Notificación masiva
        if self.token_repo:
            tokens = self.token_repo.get_all_tokens()
            for t in tokens:
                if t.fcm_token:
                    firebase_client.send_notification(
                        t.fcm_token,
                        "⚠️ ESTADO DE EMERGENCIA",
                        contenido
                    )
                    
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
        return ComunicadoResponse(id_comunicado=m.id_comunicado, titulo=m.titulo, contenido=m.contenido, id_autor=m.id_autor, autor_nombre=nombre, fecha_publicacion=m.fecha_publicacion, fecha_vigencia=m.fecha_vigencia)