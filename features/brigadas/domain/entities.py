from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
import uuid

class BrigadaCreate(BaseModel):
    nombre: str
    id_coordinador: Optional[str] = None

class BrigadaAssignMember(BaseModel):
    id_brigadista: str

class BrigadaResponse(BaseModel):
    id_brigada: uuid.UUID
    nombre: str
    id_coordinador: Optional[str]
    coordinador_nombre: Optional[str] = None # Extraído dinámicamente de Auth
    activa: bool
    creado_en: datetime
    brigadistas: List[str] = [] # Lista de UUIDs de usuarios

    model_config = ConfigDict(from_attributes=True)
