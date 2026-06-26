from pydantic import BaseModel, EmailStr, Field, ConfigDict
from uuid import UUID
from datetime import datetime

class UsuarioCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72, description="Máximo 72 caracteres soportados por Bcrypt")
    rol: str = Field(..., pattern="^(Admin|Coordinador|Analista|Brigadista)$")

class UsuarioUpdate(BaseModel):
    rol: str = Field(None, pattern="^(Admin|Coordinador|Analista|Brigadista)$")
    activo: bool = None

# Response Model estricto: NUNCA incluye password_hash (Regla de Seguridad: Data Leakage)
class UsuarioResponse(BaseModel):
    id_usuario: UUID
    nombre: str
    email: EmailStr
    rol: str
    activo: bool
    creado_en: datetime

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str
