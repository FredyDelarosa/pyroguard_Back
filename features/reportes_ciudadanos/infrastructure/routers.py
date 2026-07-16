from fastapi import APIRouter, Depends, HTTPException, Request, status
from typing import List
from sqlalchemy.orm import Session
from core.db.connection import get_db
from core.middleware.auth import require_role, UserContext
from core.middleware.rate_limiter import limiter
from features.reportes_ciudadanos.domain.entities import ReporteCiudadanoCreate, ReporteCiudadanoResponse, ReporteCiudadanoUpdate
from features.reportes_ciudadanos.infrastructure.repositories import ReporteCiudadanoRepositoryImpl
from features.reportes_ciudadanos.application.usecases import ReporteCiudadanoUseCase
from core.utils.ml_client import MLServiceClient

router = APIRouter(prefix="/api", tags=["Reportes Ciudadanos (Modular)"])

def get_usecase(db: Session = Depends(get_db)):
    return ReporteCiudadanoUseCase(ReporteCiudadanoRepositoryImpl(db))

@router.post("/reportes", response_model=ReporteCiudadanoResponse)
@limiter.limit("5/minute")
def crear_reporte(request: Request, reporte_in: ReporteCiudadanoCreate, usecase: ReporteCiudadanoUseCase = Depends(get_usecase)):
    return usecase.crear(reporte_in)

@router.get("/reportes", response_model=List[ReporteCiudadanoResponse])
def listar_reportes(
    usecase: ReporteCiudadanoUseCase = Depends(get_usecase),
    current_user: UserContext = Depends(require_role(["Admin", "Coordinador"]))
):
    return usecase.listar()

@router.put("/reportes/{id_reporte}/estado", response_model=ReporteCiudadanoResponse)
def actualizar_estado_reporte(
    id_reporte: str, 
    update_in: ReporteCiudadanoUpdate, 
    usecase: ReporteCiudadanoUseCase = Depends(get_usecase),
    current_user: UserContext = Depends(require_role(["Admin", "Coordinador"]))
):
    res = usecase.update_estado(id_reporte, update_in.estado)
    if not res: 
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    return res

@router.get("/clima/{id_zona}")
async def consultar_clima_ciudadano(id_zona: str):
    ml_client = MLServiceClient()
    clima = await ml_client.get_weather_for_zone(id_zona)
    if not clima: 
        raise HTTPException(status_code=404, detail="No se pudo obtener el clima de esta zona")
    return clima
