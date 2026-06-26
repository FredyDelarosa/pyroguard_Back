from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from domain.model.reporte import ReporteCiudadanoCreate, ReporteCiudadanoResponse
from core.middleware.auth import require_role
from core.middleware.rate_limiter import limiter
from infrastructure.dependencies import get_reporte_ciudadano_usecase
from application.usecase.reporte_ciudadano_usecase import ReporteCiudadanoUseCase
from core.utils.ml_client import MLServiceClient

router = APIRouter()

@router.post("/reportes", response_model=ReporteCiudadanoResponse)
@limiter.limit("5/minute")
def crear_reporte(request: Request, reporte_in: ReporteCiudadanoCreate, usecase: ReporteCiudadanoUseCase = Depends(get_reporte_ciudadano_usecase)):
    return usecase.crear(reporte_in)

@router.get("/reportes", response_model=List[ReporteCiudadanoResponse])
def listar_reportes(usecase: ReporteCiudadanoUseCase = Depends(get_reporte_ciudadano_usecase), current_user = Depends(require_role(["Admin", "Coordinador"]))):
    return usecase.listar()

from domain.model.reporte import ReporteCiudadanoUpdate
@router.put("/reportes/{id_reporte}/estado", response_model=ReporteCiudadanoResponse)
def actualizar_estado_reporte(id_reporte: str, update_in: ReporteCiudadanoUpdate, usecase: ReporteCiudadanoUseCase = Depends(get_reporte_ciudadano_usecase), current_user = Depends(require_role(["Admin", "Coordinador"]))):
    res = usecase.update_estado(id_reporte, update_in.estado)
    if not res: raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return res

@router.get("/clima/{id_zona}")
async def consultar_clima_ciudadano(id_zona: str):
    ml_client = MLServiceClient()
    clima = await ml_client.get_weather_for_zone(id_zona)
    if not clima: raise HTTPException(status_code=404, detail="No se pudo obtener el clima de esta zona")
    return clima
