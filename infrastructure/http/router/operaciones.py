from fastapi import APIRouter, Depends, HTTPException
from typing import List
from domain.model.intervencion import IntervencionCreate, IntervencionUpdate, IntervencionResponse
from infrastructure.database.postgres.models import Usuario
from core.middleware.auth import require_role
from infrastructure.dependencies import get_intervencion_usecase
from application.usecase.intervencion_usecase import IntervencionUseCase

router = APIRouter()

@router.post("/intervenciones", response_model=IntervencionResponse)
def crear_intervencion(intervencion_in: IntervencionCreate, usecase: IntervencionUseCase = Depends(get_intervencion_usecase), current_user: Usuario = Depends(require_role(["Admin", "Coordinador"]))):
    return usecase.crear(intervencion_in, str(current_user.id_usuario))

@router.put("/intervenciones/{id_intervencion}", response_model=IntervencionResponse)
def actualizar_intervencion(id_intervencion: str, intervencion_in: IntervencionUpdate, usecase: IntervencionUseCase = Depends(get_intervencion_usecase), current_user: Usuario = Depends(require_role(["Admin", "Coordinador", "Brigadista"]))):
    res = usecase.actualizar(id_intervencion, intervencion_in)
    if not res: raise HTTPException(status_code=404, detail="Intervención no encontrada")
    return res

@router.get("/intervenciones/zona/{id_zona}", response_model=List[IntervencionResponse])
def historial_intervenciones_zona(id_zona: str, limit: int = 5, usecase: IntervencionUseCase = Depends(get_intervencion_usecase), current_user: Usuario = Depends(require_role(["Admin", "Coordinador", "Brigadista"]))):
    return usecase.historial_zona(id_zona, limit)
