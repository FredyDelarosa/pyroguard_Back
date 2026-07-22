from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from core.db.connection import get_db
from core.middleware.auth import require_role, UserContext
from features.comunicados.domain.entities import ComunicadoCreate, ComunicadoResponse, EmergenciaCreate
from features.comunicados.infrastructure.repositories import ComunicadoRepositoryImpl
from features.notificaciones.infrastructure.repositories import DeviceTokenRepositoryImpl
from features.comunicados.application.usecases import ComunicadoUseCase

router = APIRouter(tags=["Comunicados (Modular)"])
def get_usecase(db: Session = Depends(get_db)): 
    return ComunicadoUseCase(
        ComunicadoRepositoryImpl(db),
        DeviceTokenRepositoryImpl(db)
    )

@router.post("/comunicados", response_model=ComunicadoResponse)
def crear(comunicado_in: ComunicadoCreate, usecase: ComunicadoUseCase = Depends(get_usecase), current_user: UserContext = Depends(require_role(["Admin"]))):
    return usecase.crear(comunicado_in, current_user.id_usuario)

@router.get("/comunicados", response_model=List[ComunicadoResponse])
def listar(usecase: ComunicadoUseCase = Depends(get_usecase)):
    return usecase.listar()

@router.post("/comunicados/emergencia", response_model=ComunicadoResponse)
def declarar_emergencia(
    emergencia_in: EmergenciaCreate, 
    usecase: ComunicadoUseCase = Depends(get_usecase), 
    current_user: UserContext = Depends(require_role(["Admin"]))
):
    return usecase.declarar_emergencia(emergencia_in, current_user.id_usuario)