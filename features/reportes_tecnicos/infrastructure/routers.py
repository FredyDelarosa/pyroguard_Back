from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from core.db.connection import get_db
from core.middleware.auth import require_role, UserContext
from features.reportes_tecnicos.domain.entities import ReporteTecnicoSolicitar, ReporteTecnicoResponse, WebhookPayload
from features.reportes_tecnicos.infrastructure.repositories import ReporteTecnicoRepositoryImpl
from features.notificaciones.infrastructure.repositories import DeviceTokenRepositoryImpl
from features.reportes_tecnicos.application.usecases import ReporteTecnicoUseCase

router = APIRouter(tags=["Reportes Tecnicos (Modular)"])
def get_usecase(db: Session = Depends(get_db)): 
    return ReporteTecnicoUseCase(
        ReporteTecnicoRepositoryImpl(db),
        DeviceTokenRepositoryImpl(db)
    )

@router.post("/reportes_tecnicos/solicitar", response_model=ReporteTecnicoResponse)
def solicitar_generacion(
    r: ReporteTecnicoSolicitar, 
    usecase: ReporteTecnicoUseCase = Depends(get_usecase), 
    current_user: UserContext = Depends(require_role(["Admin", "Coordinador"]))
):
    try:
        return usecase.solicitar_generacion(r, current_user.id_usuario)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reportes_tecnicos/webhook", status_code=200)
def webhook_ml(
    payload: WebhookPayload, 
    usecase: ReporteTecnicoUseCase = Depends(get_usecase)
):
    # Este endpoint es llamado internamente por Celery/ML, no requiere JWT del usuario.
    try:
        usecase.procesar_webhook(payload)
        return {"status": "ok"}
    except Exception as e:
        print(f"Error procesando webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/reportes_tecnicos/zona/{id_zona}", response_model=List[ReporteTecnicoResponse])
def listar(
    id_zona: str, 
    usecase: ReporteTecnicoUseCase = Depends(get_usecase), 
    current_user: UserContext = Depends(require_role(["Admin", "Coordinador"]))
):
    return usecase.listar(id_zona)