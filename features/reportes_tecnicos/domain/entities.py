from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional, List, Dict, Any

class ReporteTecnicoSolicitar(BaseModel):
    id_zona: UUID

class ReporteTecnicoResponse(BaseModel):
    id_reporte: UUID
    id_zona: UUID
    id_coordinador: Optional[str]
    coordinador_nombre: Optional[str] = None
    estado: str
    task_id: Optional[str] = None
    nivel_riesgo_registrado: Optional[str] = None
    archivo_pdf_path: Optional[str] = None
    creado_en: datetime
    
    model_config = ConfigDict(from_attributes=True)

class AccionTactico(BaseModel):
    accion: str
    fuente: Optional[str] = None

class ReporteLLM(BaseModel):
    resumen_ejecutivo: str
    analisis_de_riesgo: str
    justificacion_protocolo: str
    acciones_tacticas: List[AccionTactico]
    evaluacion_matematica: Dict[str, Any]

class WebhookPayload(BaseModel):
    id_zona: str
    task_id: str
    reporte_json: ReporteLLM