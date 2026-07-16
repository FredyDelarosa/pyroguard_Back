from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class IntervencionCreate(BaseModel):
    id_brigada: UUID
    id_zona: UUID
    estado: str = "Pendiente"
    observaciones: Optional[str] = None

class IntervencionUpdate(BaseModel):
    estado: str
    observaciones: Optional[str] = None

class IntervencionResponse(BaseModel):
    id_intervencion: UUID
    id_brigada: UUID
    id_zona: UUID
    estado: str
    observaciones: Optional[str]
    fecha_asignacion: datetime
    fecha_completada: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)