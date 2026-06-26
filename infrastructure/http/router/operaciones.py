from fastapi import APIRouter, Depends, HTTPException
from typing import List
from domain.model.intervencion import IntervencionCreate, IntervencionUpdate, IntervencionResponse
from infrastructure.database.postgres.models import Usuario
from core.middleware.auth import require_role
from infrastructure.dependencies import get_intervencion_usecase, get_brigada_usecase
from application.usecase.intervencion_usecase import IntervencionUseCase
from application.usecase.brigada_usecase import BrigadaUseCase
from domain.model.brigada import BrigadaCreate, BrigadaResponse, BrigadaAssignMember

router = APIRouter()

# --- BRIGADAS ---

@router.post("/brigadas", response_model=BrigadaResponse)
def crear_brigada(
    brigada_in: BrigadaCreate, 
    usecase: BrigadaUseCase = Depends(get_brigada_usecase), 
    current_user: Usuario = Depends(require_role(["Admin", "Coordinador"]))
):
    return usecase.crear_brigada(brigada_in)

@router.get("/brigadas", response_model=List[BrigadaResponse])
def listar_brigadas(
    usecase: BrigadaUseCase = Depends(get_brigada_usecase),
    current_user: Usuario = Depends(require_role(["Admin", "Coordinador"]))
):
    return usecase.listar_brigadas()

@router.post("/brigadas/{id_brigada}/miembros")
def asignar_miembro_brigada(
    id_brigada: str,
    asignacion: BrigadaAssignMember,
    usecase: BrigadaUseCase = Depends(get_brigada_usecase),
    current_user: Usuario = Depends(require_role(["Admin", "Coordinador"]))
):
    if not usecase.asignar_brigadista(id_brigada, str(asignacion.id_brigadista)):
        raise HTTPException(status_code=400, detail="Brigada o Brigadista no encontrado, o el usuario no tiene rol de Brigadista.")
    return {"status": "success", "message": "Brigadista asignado correctamente a la brigada."}

# --- INTERVENCIONES ---

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
