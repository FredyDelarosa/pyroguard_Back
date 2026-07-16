from typing import Optional, List
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from core.env import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class UserContext:
    def __init__(self, id_usuario: str, roles: List[str]):
        self.id_usuario = id_usuario
        self.roles = roles

def get_current_user(token: str = Depends(oauth2_scheme)) -> UserContext:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Validación pura (cero latencia de base de datos)
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id_str: str = payload.get("sub")
        roles: List[str] = payload.get("roles", [])
        
        if user_id_str is None:
            raise credentials_exception
            
        return UserContext(id_usuario=user_id_str, roles=roles)
    except JWTError:
        raise credentials_exception

def require_role(roles_permitidos: list[str]):
    """
    Dependencia inyectable que valida si el usuario tiene uno de los roles requeridos,
    basado puramente en lo que firmó el Auth Service en el JWT.
    """
    def role_checker(current_user: UserContext = Depends(get_current_user)):
        # Si el usuario tiene al menos uno de los roles permitidos
        if not any(rol in roles_permitidos for rol in current_user.roles):
            # Para retrocompatibilidad si venia como string "rol" en payloads viejos
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos suficientes para realizar esta acción."
            )
        return current_user
    return role_checker
