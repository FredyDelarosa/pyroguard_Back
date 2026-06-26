from fastapi import APIRouter, Depends, HTTPException
from typing import List

from infrastructure.database.postgres.models import Usuario
from domain.model.comunicado import ComunicadoCreate, ComunicadoResponse
from core.middleware.auth import get_current_user, require_role
from infrastructure.dependencies import get_comunicado_usecase
from application.usecase.comunicado_usecase import ComunicadoUseCase

router = APIRouter()

@router.post("/", response_model=ComunicadoResponse)
def publicar_comunicado(
    comunicado_in: ComunicadoCreate,
    usecase: ComunicadoUseCase = Depends(get_comunicado_usecase),
    current_user: Usuario = Depends(require_role(["Admin"]))
):
    return usecase.crear_comunicado(comunicado_in, str(current_user.id_usuario))

@router.get("/activos", response_model=List[ComunicadoResponse])
def listar_comunicados_activos(
    usecase: ComunicadoUseCase = Depends(get_comunicado_usecase)
):
    return usecase.obtener_activos()

@router.get("/historial", response_model=List[ComunicadoResponse])
def historial_comunicados(
    usecase: ComunicadoUseCase = Depends(get_comunicado_usecase),
    current_user: Usuario = Depends(require_role(["Admin"]))
):
    return usecase.obtener_todos()

@router.delete("/{id_comunicado}")
def eliminar_comunicado(
    id_comunicado: str,
    usecase: ComunicadoUseCase = Depends(get_comunicado_usecase),
    current_user: Usuario = Depends(require_role(["Admin"]))
):
    if not usecase.borrar_comunicado(id_comunicado):
        raise HTTPException(status_code=404, detail="Comunicado no encontrado")
    return {"status": "success", "message": "Comunicado eliminado correctamente"}
