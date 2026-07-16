import requests
from typing import Optional
from core.env import settings

class CryptoServiceClient:
    def __init__(self):
        self.base_url = settings.CRYPTO_SERVICE_URL
        self.api_key = settings.API_KEY
        self.headers = {"X-API-KEY": self.api_key}

    def encrypt(self, data: str) -> str:
        try:
            response = requests.post(
                f"{self.base_url}/v1/encrypt",
                json={"plaintext": data},
                headers=self.headers,
                timeout=5
            )
            response.raise_for_status()
            return response.json()["result"]
        except Exception as e:
            raise ValueError(f"Fallo al cifrar datos: {e}")

    def decrypt(self, ciphertext: str) -> str:
        try:
            response = requests.post(
                f"{self.base_url}/v1/decrypt",
                json={"ciphertext": ciphertext},
                headers=self.headers,
                timeout=5
            )
            response.raise_for_status()
            return response.json()["result"]
        except Exception as e:
            raise ValueError(f"Fallo al descifrar datos: {e}")

crypto_client = CryptoServiceClient()
