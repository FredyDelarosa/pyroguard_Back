from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from core.db.connection import get_db
from core.middleware.auth import require_role, UserContext
from features.reportes_tecnicos.domain.entities import ReporteTecnicoCreate, ReporteTecnicoResponse
from features.reportes_tecnicos.infrastructure.repositories import ReporteTecnicoRepositoryImpl
from features.reportes_tecnicos.application.usecases import ReporteTecnicoUseCase

router = APIRouter(prefix="/api", tags=["Reportes Tecnicos (Modular)"])
def get_usecase(db: Session = Depends(get_db)): return ReporteTecnicoUseCase(ReporteTecnicoRepositoryImpl(db))

@router.post("/reportes_tecnicos", response_model=ReporteTecnicoResponse)
def generar(r: ReporteTecnicoCreate, usecase: ReporteTecnicoUseCase = Depends(get_usecase), current_user: UserContext = Depends(require_role(["Admin", "Coordinador"]))):
    return usecase.generar(r, current_user.id_usuario)

@router.get("/reportes_tecnicos/zona/{id_zona}", response_model=List[ReporteTecnicoResponse])
def listar(id_zona: str, usecase: ReporteTecnicoUseCase = Depends(get_usecase), current_user: UserContext = Depends(require_role(["Admin", "Coordinador"]))):
    return usecase.listar(id_zona)