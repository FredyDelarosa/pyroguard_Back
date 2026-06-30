import base64
from typing import Optional
from core.security.crypto import ICryptoProvider

class CipherPipe:
    def __init__(self, crypto_provider: ICryptoProvider):
        self.crypto_provider = crypto_provider
        self.prefix = "enc::v1::"

    def execute(self, data: Optional[str]) -> Optional[str]:
        if not data:
            return data
        
        # Evitar doble cifrado si ya está cifrado
        if str(data).startswith(self.prefix):
            return data
            
        encrypted_bytes = self.crypto_provider.encrypt(str(data).encode('utf-8'))
        payload = base64.b64encode(encrypted_bytes).decode('utf-8')
        return f"{self.prefix}{payload}"

class DecryptPipe:
    def __init__(self, crypto_provider: ICryptoProvider):
        self.crypto_provider = crypto_provider
        self.prefix = "enc::v1::"

    def execute(self, data: Optional[str]) -> Optional[str]:
        if not data or not isinstance(data, str) or not data.startswith(self.prefix):
            return data
            
        # Remover el prefijo
        payload = data[len(self.prefix):]
        try:
            encrypted_bytes = base64.b64decode(payload)
            decrypted_bytes = self.crypto_provider.decrypt(encrypted_bytes)
            return decrypted_bytes.decode('utf-8')
        except Exception:
            raise ValueError("Fallo de integridad al descifrar el campo.")
