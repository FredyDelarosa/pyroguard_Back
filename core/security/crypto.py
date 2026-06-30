from abc import ABC, abstractmethod
import secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class ICryptoProvider(ABC):
    @abstractmethod
    def encrypt(self, data: bytes) -> bytes:
        pass

    @abstractmethod
    def decrypt(self, encrypted_data: bytes) -> bytes:
        pass

class AESGCMCryptoProvider(ICryptoProvider):
    def __init__(self, key: bytes):
        if len(key) not in (16, 24, 32):
            raise ValueError("La llave debe ser de 16, 24 o 32 bytes para AES")
        self.aesgcm = AESGCM(key)

    def encrypt(self, data: bytes) -> bytes:
        nonce = secrets.token_bytes(12)
        ciphertext = self.aesgcm.encrypt(nonce, data, None)
        return nonce + ciphertext

    def decrypt(self, encrypted_data: bytes) -> bytes:
        if len(encrypted_data) < 12:
            raise ValueError("Datos cifrados corruptos o demasiado cortos")
        nonce = encrypted_data[:12]
        ciphertext = encrypted_data[12:]
        return self.aesgcm.decrypt(nonce, ciphertext, None)
