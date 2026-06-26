from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from typing import List
import os
from domain.model.reporte import ReporteTecnicoCreate, ReporteTecnicoResponse
from infrastructure.database.postgres.models import Usuario
from core.middleware.auth import get_current_user, require_role
from infrastructure.dependencies import get_reporte_tecnico_usecase
from application.usecase.reporte_tecnico_usecase import ReporteTecnicoUseCase

router = APIRouter()

@router.post("/tecnicos", response_model=ReporteTecnicoResponse)
def generar_reporte_tecnico(reporte_in: ReporteTecnicoCreate, usecase: ReporteTecnicoUseCase = Depends(get_reporte_tecnico_usecase), current_user: Usuario = Depends(require_role(["Admin", "Coordinador"]))):
    return usecase.generar(reporte_in, str(current_user.id_usuario), current_user.nombre)

@router.get("/tecnicos", response_model=List[ReporteTecnicoResponse])
def listar_reportes_tecnicos(usecase: ReporteTecnicoUseCase = Depends(get_reporte_tecnico_usecase), current_user: Usuario = Depends(require_role(["Admin", "Coordinador", "Analista"]))):
    return usecase.listar()

@router.get("/tecnicos/{id_reporte}/descargar")
def descargar_reporte_tecnico(id_reporte: str, usecase: ReporteTecnicoUseCase = Depends(get_reporte_tecnico_usecase), current_user: Usuario = Depends(get_current_user)):
    pdf_path = usecase.obtener_archivo(id_reporte)
    if not pdf_path: raise HTTPException(status_code=404, detail="Reporte no encontrado")
    if not os.path.exists(pdf_path): raise HTTPException(status_code=404, detail="El archivo físico ya no existe")
    return FileResponse(path=pdf_path, filename=os.path.basename(pdf_path), media_type='application/pdf')
