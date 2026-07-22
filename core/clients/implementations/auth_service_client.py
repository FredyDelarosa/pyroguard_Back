import requests
from typing import Optional, Dict, Any
from core.env import settings

class AuthServiceClient:
    def __init__(self):
        self.base_url = settings.AUTH_SERVICE_URL
        self.api_key = settings.API_KEY
        self.headers = {"X-API-KEY": self.api_key}

    def get_user_info(self, user_id: str) -> Optional[Dict[str, Any]]:
        try:
            response = requests.get(
                f"{self.base_url}/auth/internal/users/{user_id}",
                headers=self.headers,
                timeout=5
            )
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise ValueError(f"No se pudo obtener la información del usuario {user_id}: {e}")

auth_client = AuthServiceClient()
