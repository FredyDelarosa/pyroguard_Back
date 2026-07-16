from core.security.pipeline import CipherPipe, DecryptPipe
from core.security.interceptor import PersistenceInterceptor

# Instanciación de dependencias (Factory)
_cipher_pipe = CipherPipe()
_decrypt_pipe = DecryptPipe()

# Este es el interceptor que los repositorios importarán y usarán
persistence_interceptor = PersistenceInterceptor(_cipher_pipe, _decrypt_pipe)
