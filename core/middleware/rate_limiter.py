from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI

# Configuración del limitador global (Anti-Spam)
limiter = Limiter(key_func=get_remote_address)

def setup_rate_limiter(app: FastAPI):
    """
    Registra el middleware de Rate Limiting en la aplicación FastAPI.
    """
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
