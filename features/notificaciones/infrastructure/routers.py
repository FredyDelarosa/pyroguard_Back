from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from core.db.connection import get_db
from features.notificaciones.domain.entities import DeviceTokenCreate, DeviceTokenResponse, AlertaCriticidadRequest
from features.notificaciones.infrastructure.repositories import DeviceTokenRepositoryImpl
from features.notificaciones.application.usecases import NotificacionesUseCase
from core.middleware.auth import require_role, UserContext
from core.env import settings

router = APIRouter(tags=["Notificaciones (FCM)"])

def get_notificaciones_usecase(db: Session = Depends(get_db)):
    repo = DeviceTokenRepositoryImpl(db)
    return NotificacionesUseCase(repo)

@router.post("/notificaciones/token", response_model=DeviceTokenResponse)
def registrar_token(
    req: DeviceTokenCreate, 
    usecase: NotificacionesUseCase = Depends(get_notificaciones_usecase),
    current_user: UserContext = Depends(require_role(["Admin", "Coordinador", "Brigadista"]))
):
    return usecase.registrar_token(req)

@router.post("/notificaciones/alertas-criticidad", status_code=status.HTTP_200_OK)
def recibir_alerta_criticidad(
    req: AlertaCriticidadRequest,
    x_api_key: str = Header(...),
    usecase: NotificacionesUseCase = Depends(get_notificaciones_usecase)
):
    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return usecase.enviar_alerta_general(req)
