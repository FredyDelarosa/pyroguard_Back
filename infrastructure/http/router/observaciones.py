from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from infrastructure.database.postgres.models import Usuario
from domain.model.observacion import ObservacionCampoCreate, ObservacionCampoResponse
from core.middleware.auth import get_current_user, require_role
from infrastructure.dependencies import get_observacion_usecase
from application.usecase.observacion_usecase import ObservacionUseCase

router = APIRouter()

@router.post("/", response_model=ObservacionCampoResponse, status_code=status.HTTP_201_CREATED)
def registrar_observacion_campo(
    observacion_in: ObservacionCampoCreate,
    usecase: ObservacionUseCase = Depends(get_observacion_usecase),
    current_user: Usuario = Depends(require_role(["Brigadista", "Admin"]))
):
    """
    Registra una observación en campo. Solo accesible por Brigadistas o Admins.
    """
    return usecase.registrar_observacion(observacion_in, str(current_user.id_usuario))

@router.get("/zona/{id_zona}", response_model=List[ObservacionCampoResponse])
def obtener_observaciones_por_zona(
    id_zona: str,
    usecase: ObservacionUseCase = Depends(get_observacion_usecase),
    current_user: Usuario = Depends(require_role(["Coordinador", "Admin"]))
):
    """
    Permite al coordinador consultar las observaciones hechas en una zona específica.
    """
    return usecase.listar_por_zona(id_zona)
