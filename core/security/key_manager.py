import hashlib
from core.env import settings

class KeyManager:
    def get_master_key(self) -> bytes:
        secret_key = settings.SECRET_KEY
        return hashlib.sha256(secret_key.encode('utf-8')).digest()
