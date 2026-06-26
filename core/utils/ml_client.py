import httpx
from core.env import settings
import logging

logger = logging.getLogger(__name__)

class MLServiceClient:
    """
    Cliente HTTP interno para comunicarse con el Microservicio de Machine Learning.
    Esto permite mantener las bases de datos separadas (Arquitectura de Microservicios).
    """
    def __init__(self):
        self.base_url = settings.ML_SERVICE_URL
        self.timeout = httpx.Timeout(10.0) # 10 segundos máximo para evitar colgar al backend

    async def get_prediction_history(self, limit: int = 20):
        """
        Consulta el historial de predicciones de riesgo del microservicio ML.
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                # Se asume que el endpoint en el ML service es /api/v1/predict/history
                response = await client.get(f"{self.base_url}/api/v1/predict/history?limit={limit}")
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as exc:
                logger.error(f"Error de red al conectar con ML Service: {exc}")
                return []
            except httpx.HTTPStatusError as exc:
                logger.error(f"Error HTTP {exc.response.status_code} devuelto por ML Service")
                return []

    async def get_weather_for_zone(self, id_zona: str):
        """
        Consulta el clima actual de una zona en el microservicio ML.
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(f"{self.base_url}/api/v1/zonas/{id_zona}/clima")
                response.raise_for_status()
                return response.json()
            except Exception as exc:
                logger.error(f"Error al conectar con ML Service para clima: {exc}")
                return None
