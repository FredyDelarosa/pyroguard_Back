from pydantic import BaseModel, ConfigDict
from uuid import UUID

class DeviceTokenCreate(BaseModel):
    id_usuario: str
    fcm_token: str

class DeviceTokenResponse(BaseModel):
    id_usuario: str
    fcm_token: str
    
    model_config = ConfigDict(from_attributes=True)

class AlertaCriticidadRequest(BaseModel):
    id_zona: str
    nivel_riesgo: str
    mensaje: str
