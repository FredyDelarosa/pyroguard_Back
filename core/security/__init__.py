from core.security.crypto import AESGCMCryptoProvider
from core.security.key_manager import KeyManager
from core.security.pipeline import CipherPipe, DecryptPipe
from core.security.interceptor import PersistenceInterceptor

# Instanciación de dependencias (Factory)
# En un proyecto con un contenedor de dependencias (Dependency Injector),
# esto se configuraría allí. Por simplicidad, exponemos una instancia singleton.

_key_manager = KeyManager()
_master_key = _key_manager.get_master_key()
_crypto_provider = AESGCMCryptoProvider(_master_key)

_cipher_pipe = CipherPipe(_crypto_provider)
_decrypt_pipe = DecryptPipe(_crypto_provider)

# Este es el interceptor que los repositorios importarán y usarán
persistence_interceptor = PersistenceInterceptor(_cipher_pipe, _decrypt_pipe)
