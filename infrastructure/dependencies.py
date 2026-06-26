from fastapi import Depends
from sqlalchemy.orm import Session
from core.db.connection import get_db

from infrastructure.database.postgres.usuario_repository_impl import UsuarioRepositoryImpl
from application.usecase.usuario_usecase import UsuarioUseCase

def get_usuario_repository(db: Session = Depends(get_db)) -> UsuarioRepositoryImpl:
    return UsuarioRepositoryImpl(db)

def get_usuario_usecase(repo: UsuarioRepositoryImpl = Depends(get_usuario_repository)) -> UsuarioUseCase:
    return UsuarioUseCase(repo)

from infrastructure.database.postgres.comunicado_repository_impl import ComunicadoRepositoryImpl
from application.usecase.comunicado_usecase import ComunicadoUseCase

def get_comunicado_repository(db: Session = Depends(get_db)) -> ComunicadoRepositoryImpl:
    return ComunicadoRepositoryImpl(db)

def get_comunicado_usecase(repo: ComunicadoRepositoryImpl = Depends(get_comunicado_repository)) -> ComunicadoUseCase:
    return ComunicadoUseCase(repo)

from application.usecase.auth_usecase import AuthUseCase
def get_auth_usecase(repo: UsuarioRepositoryImpl = Depends(get_usuario_repository)) -> AuthUseCase:
    return AuthUseCase(repo)

from infrastructure.database.postgres.intervencion_repository_impl import IntervencionRepositoryImpl
from application.usecase.intervencion_usecase import IntervencionUseCase
def get_intervencion_repository(db: Session = Depends(get_db)) -> IntervencionRepositoryImpl: return IntervencionRepositoryImpl(db)
def get_intervencion_usecase(repo: IntervencionRepositoryImpl = Depends(get_intervencion_repository)) -> IntervencionUseCase: return IntervencionUseCase(repo)

from infrastructure.database.postgres.reporte_ciudadano_repository_impl import ReporteCiudadanoRepositoryImpl
from application.usecase.reporte_ciudadano_usecase import ReporteCiudadanoUseCase
def get_reporte_ciudadano_repository(db: Session = Depends(get_db)) -> ReporteCiudadanoRepositoryImpl: return ReporteCiudadanoRepositoryImpl(db)
def get_reporte_ciudadano_usecase(repo: ReporteCiudadanoRepositoryImpl = Depends(get_reporte_ciudadano_repository)) -> ReporteCiudadanoUseCase: return ReporteCiudadanoUseCase(repo)

from infrastructure.database.postgres.reporte_tecnico_repository_impl import ReporteTecnicoRepositoryImpl
from application.usecase.reporte_tecnico_usecase import ReporteTecnicoUseCase
def get_reporte_tecnico_repository(db: Session = Depends(get_db)) -> ReporteTecnicoRepositoryImpl: return ReporteTecnicoRepositoryImpl(db)
def get_reporte_tecnico_usecase(repo: ReporteTecnicoRepositoryImpl = Depends(get_reporte_tecnico_repository)) -> ReporteTecnicoUseCase: return ReporteTecnicoUseCase(repo)
