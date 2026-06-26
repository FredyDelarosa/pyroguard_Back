from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class BrigadaCreate(BaseModel):
    nombre: str
    id_coordinador: Optional[UUID] = None

class BrigadaResponse(BaseModel):
    id_brigada: UUID
    nombre: str
    id_coordinador: Optional[UUID]
    activa: bool
    creado_en: datetime

    model_config = ConfigDict(from_attributes=True)
