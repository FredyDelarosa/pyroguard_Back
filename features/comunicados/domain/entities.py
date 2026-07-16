from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class ComunicadoCreate(BaseModel):
    titulo: str
    contenido: str
    fecha_vigencia: datetime

class ComunicadoResponse(BaseModel):
    id_comunicado: UUID
    titulo: str
    contenido: str
    id_autor: Optional[str]
    autor_nombre: Optional[str] = None
    fecha_publicacion: datetime
    fecha_vigencia: datetime
    
    model_config = ConfigDict(from_attributes=True)