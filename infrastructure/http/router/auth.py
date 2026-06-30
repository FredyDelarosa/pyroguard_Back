from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from domain.model.usuario import UsuarioCreate, UsuarioResponse, Token, LoginResponse
from infrastructure.dependencies import get_auth_usecase
from application.usecase.auth_usecase import AuthUseCase

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    usecase: AuthUseCase = Depends(get_auth_usecase)
):
    token, usuario = usecase.autenticar_usuario(form_data.username, form_data.password)
    if token == "INACTIVO":
        raise HTTPException(status_code=403, detail="Usuario inactivo")
    if not token:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return {"access_token": token, "token_type": "bearer", "usuario": usuario}

@router.post("/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def register(
    usuario_in: UsuarioCreate,
    usecase: AuthUseCase = Depends(get_auth_usecase)
):
    usuario = usecase.registrar_usuario(usuario_in)
    if not usuario:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    return usuario
