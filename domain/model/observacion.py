from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class ObservacionCampoCreate(BaseModel):
    id_zona: UUID = Field(..., description="UUID de la zona donde se hace la observación")
    latitud: float = Field(..., description="Latitud GPS capturada por el móvil")
    longitud: float = Field(..., description="Longitud GPS capturada por el móvil")
    condiciones: str = Field(..., description="Condición predefinida (ej. Terreno inestable, Fuego activo, Favorable)")
    recursos_necesarios: Optional[str] = Field(None, description="Solicitud de recursos (ej. Agua, Herramientas, Apoyo aéreo)")
    observaciones_texto: str = Field(..., description="Texto libre con las observaciones detalladas del brigadista")

class ObservacionCampoResponse(BaseModel):
    id_observacion: UUID
    id_brigadista: UUID
    id_zona: UUID
    latitud: float
    longitud: float
    condiciones: str
    recursos_necesarios: Optional[str]
    observaciones_texto: str
    creado_en: datetime

    model_config = ConfigDict(from_attributes=True)
