from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.db.connection import get_db
from core.middleware.auth import require_role, UserContext
from features.brigadas.domain.entities import BrigadaCreate, BrigadaResponse, BrigadaAssignMember
from features.brigadas.infrastructure.repositories import BrigadaRepositoryImpl
from features.brigadas.application.usecases import BrigadaUseCase

router = APIRouter(prefix="/api", tags=["Brigadas (Modular)"])

def get_brigada_usecase(db: Session = Depends(get_db)):
    repo = BrigadaRepositoryImpl(db)
    return BrigadaUseCase(repo)

@router.post("/brigadas", response_model=BrigadaResponse, status_code=status.HTTP_201_CREATED)
def crear_brigada(
    brigada_in: BrigadaCreate, 
    usecase: BrigadaUseCase = Depends(get_brigada_usecase),
    current_user: UserContext = Depends(require_role(["Admin", "Coordinador"]))
):
    try:
        return usecase.crear_brigada(brigada_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/brigadas", response_model=List[BrigadaResponse])
def listar_brigadas(
    usecase: BrigadaUseCase = Depends(get_brigada_usecase),
    current_user: UserContext = Depends(require_role(["Admin", "Coordinador", "Brigadista"]))
):
    return usecase.listar_brigadas()

@router.post("/brigadas/{id_brigada}/miembros", status_code=status.HTTP_200_OK)
def asignar_miembro(
    id_brigada: str,
    payload: BrigadaAssignMember,
    usecase: BrigadaUseCase = Depends(get_brigada_usecase),
    current_user: UserContext = Depends(require_role(["Admin", "Coordinador"]))
):
    try:
        success = usecase.asignar_brigadista(id_brigada, payload.id_brigadista)
        if success:
            return {"message": "Brigadista asignado exitosamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
