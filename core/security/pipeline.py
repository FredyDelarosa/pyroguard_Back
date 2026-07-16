from typing import Optional
from core.clients.implementations.crypto_service_client import crypto_client

class CipherPipe:
    def __init__(self):
        self.prefix = "enc::v1::"

    def execute(self, data: Optional[str]) -> Optional[str]:
        if not data:
            return data
        
        # Evitar llamada HTTP si ya está cifrado localmente
        if str(data).startswith(self.prefix):
            return data
            
        return crypto_client.encrypt(str(data))

class DecryptPipe:
    def __init__(self):
        self.prefix = "enc::v1::"

    def execute(self, data: Optional[str]) -> Optional[str]:
        if not data or not isinstance(data, str) or not data.startswith(self.prefix):
            return data
            
        return crypto_client.decrypt(data)
