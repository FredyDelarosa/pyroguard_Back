from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from core.db.connection import get_db
from core.middleware.auth import require_role, UserContext
from features.observaciones.domain.entities import ObservacionCampoCreate, ObservacionCampoResponse
from features.observaciones.infrastructure.repositories import ObservacionRepositoryImpl
from features.observaciones.application.usecases import ObservacionUseCase

router = APIRouter(tags=["Observaciones (Modular)"])
def get_usecase(db: Session = Depends(get_db)): return ObservacionUseCase(ObservacionRepositoryImpl(db))

@router.post("/observaciones", response_model=ObservacionCampoResponse)
def crear(o: ObservacionCampoCreate, usecase: ObservacionUseCase = Depends(get_usecase), current_user: UserContext = Depends(require_role(["Admin", "Coordinador", "Brigadista"]))):
    return usecase.crear(o, current_user.id_usuario)

@router.get("/observaciones/zona/{id_zona}", response_model=List[ObservacionCampoResponse])
def listar(id_zona: str, usecase: ObservacionUseCase = Depends(get_usecase), current_user: UserContext = Depends(require_role(["Admin", "Coordinador", "Brigadista"]))):
    return usecase.listar_por_zona(id_zona)