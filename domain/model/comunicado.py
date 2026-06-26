from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class ComunicadoCreate(BaseModel):
    titulo: str = Field(..., min_length=5, max_length=255)
    contenido: str = Field(..., min_length=10)
    fecha_vigencia: datetime

class ComunicadoResponse(BaseModel):
    id_comunicado: UUID
    titulo: str
    contenido: str
    id_autor: Optional[UUID]
    fecha_publicacion: datetime
    fecha_vigencia: datetime

    model_config = ConfigDict(from_attributes=True)
