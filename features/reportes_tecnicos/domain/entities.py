from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class ReporteTecnicoCreate(BaseModel):
    id_zona: UUID
    nivel_riesgo_registrado: str

class ReporteTecnicoResponse(BaseModel):
    id_reporte: UUID
    id_zona: UUID
    id_coordinador: Optional[str]
    coordinador_nombre: Optional[str] = None
    nivel_riesgo_registrado: str
    archivo_pdf_path: str
    creado_en: datetime
    
    model_config = ConfigDict(from_attributes=True)