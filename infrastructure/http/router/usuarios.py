from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from core.db.connection import get_db
from infrastructure.database.postgres.models import Usuario
from domain.model.usuario import UsuarioResponse, UsuarioUpdate
from core.middleware.auth import require_role

# Clean Architecture Imports
from infrastructure.database.postgres.usuario_repository_impl import UsuarioRepositoryImpl
from application.usecase.usuario_usecase import UsuarioUseCase

router = APIRouter()

def get_usuario_usecase(db: Session = Depends(get_db)) -> UsuarioUseCase:
    """
    Inyección de Dependencias:
    Instancia la implementación concreta del repositorio y se la inyecta al Caso de Uso.
    """
    repository = UsuarioRepositoryImpl(db)
    return UsuarioUseCase(repository)

@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(
    usecase: UsuarioUseCase = Depends(get_usuario_usecase),
    current_user: Usuario = Depends(require_role(["Admin"]))
):
    """
    Lista todos los usuarios usando Clean Architecture.
    """
    return usecase.obtener_todos_los_usuarios()

@router.put("/{id_usuario}", response_model=UsuarioResponse)
def actualizar_usuario(
    id_usuario: str,
    usuario_in: UsuarioUpdate,
    usecase: UsuarioUseCase = Depends(get_usuario_usecase),
    current_user: Usuario = Depends(require_role(["Admin"]))
):
    """
    Actualiza el perfil de un usuario delegando la lógica al Caso de Uso.
    """
    usuario = usecase.modificar_usuario(id_usuario, usuario_in)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.delete("/{id_usuario}")
def eliminar_usuario(
    id_usuario: str,
    usecase: UsuarioUseCase = Depends(get_usuario_usecase),
    current_user: Usuario = Depends(require_role(["Admin"]))
):
    """
    Elimina físicamente a un usuario delegando la regla de negocio al Caso de Uso.
    """
    try:
        exito = usecase.eliminar_usuario(id_usuario, str(current_user.id_usuario))
        if not exito:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"status": "success", "message": f"Usuario {id_usuario} eliminado correctamente"}
    except ValueError as e:
        # Captura errores de regla de negocio (ej. borrar su propia cuenta)
        raise HTTPException(status_code=400, detail=str(e))
