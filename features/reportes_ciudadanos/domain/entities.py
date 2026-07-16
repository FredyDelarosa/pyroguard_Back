from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class ReporteCiudadanoCreate(BaseModel):
    descripcion: str = Field(..., min_length=10, max_length=1000)
    latitud: float = Field(..., ge=-90.0, le=90.0)
    longitud: float = Field(..., ge=-180.0, le=180.0)
    foto_url: Optional[str] = None

class ReporteCiudadanoUpdate(BaseModel):
    estado: str = Field(..., pattern="^(Pendiente|Verificado|Falsa Alarma)$")

class ReporteCiudadanoResponse(BaseModel):
    id_reporte: UUID
    descripcion: str
    latitud: float
    longitud: float
    foto_url: Optional[str]
    estado: str
    creado_en: datetime

    model_config = ConfigDict(from_attributes=True)
