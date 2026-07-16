from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class ObservacionCampoCreate(BaseModel):
    id_zona: UUID
    latitud: float
    longitud: float
    condiciones: str
    recursos_necesarios: Optional[str] = None
    observaciones_texto: Optional[str] = None

class ObservacionCampoResponse(BaseModel):
    id_observacion: UUID
    id_brigadista: Optional[str]
    brigadista_nombre: Optional[str] = None
    id_zona: UUID
    latitud: float
    longitud: float
    condiciones: str
    recursos_necesarios: Optional[str]
    observaciones_texto: Optional[str]
    creado_en: datetime
    
    model_config = ConfigDict(from_attributes=True)