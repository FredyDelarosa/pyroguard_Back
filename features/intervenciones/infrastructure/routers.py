from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from core.db.connection import get_db
from core.middleware.auth import require_role, UserContext
from features.intervenciones.domain.entities import IntervencionCreate, IntervencionUpdate, IntervencionResponse
from features.intervenciones.infrastructure.repositories import IntervencionRepositoryImpl
from features.intervenciones.application.usecases import IntervencionUseCase
from features.brigadas.infrastructure.repositories import BrigadaRepositoryImpl
from features.notificaciones.infrastructure.repositories import DeviceTokenRepositoryImpl

router = APIRouter(tags=["Intervenciones (Modular)"])
def get_usecase(db: Session = Depends(get_db)): 
    return IntervencionUseCase(
        IntervencionRepositoryImpl(db),
        BrigadaRepositoryImpl(db),
        DeviceTokenRepositoryImpl(db)
    )

@router.post("/intervenciones", response_model=IntervencionResponse)
def crear(i: IntervencionCreate, usecase: IntervencionUseCase = Depends(get_usecase), current_user: UserContext = Depends(require_role(["Admin", "Coordinador"]))):
    return usecase.crear(i)

@router.put("/intervenciones/{id}", response_model=IntervencionResponse)
def actualizar(id: str, i: IntervencionUpdate, usecase: IntervencionUseCase = Depends(get_usecase), current_user: UserContext = Depends(require_role(["Admin", "Coordinador", "Brigadista"]))):
    r = usecase.actualizar(id, i)
    if not r: raise HTTPException(404, "Not found")
    return r

@router.get("/intervenciones/zona/{id_zona}", response_model=List[IntervencionResponse])
def historial(id_zona: str, limit: int = 5, usecase: IntervencionUseCase = Depends(get_usecase), current_user: UserContext = Depends(require_role(["Admin", "Coordinador", "Brigadista"]))):
    return usecase.historial_zona(id_zona, limit)