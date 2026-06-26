from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.http.router import auth, operaciones, ciudadano, comunicados, usuarios
from core.middleware.rate_limiter import setup_rate_limiter

app = FastAPI(
    title="PyroGuard AI - Backend Operativo",
    description="Microservicio Principal para la gestión de Brigadas, Usuarios y Reportes. (Arquitectura Hexagonal/Clean)",
    version="1.0.0"
)

# Configurar Limiter Global
setup_rate_limiter(app)

# Configuración de CORS estricta basada en SECURITY_GUIDELINES.md
# En producción, esto debe restringirse solo a los dominios del Frontend Oficial.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # TODO: Cambiar en producción por la lista blanca exacta.
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Registrar Rutas
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Autenticación de Usuarios"])
app.include_router(usuarios.router, prefix="/api/v1/usuarios", tags=["Gestión de Usuarios (Admin)"])
app.include_router(operaciones.router, prefix="/api/v1/operaciones", tags=["Operaciones en Campo (Brigadas y Riesgo)"])
app.include_router(ciudadano.router, prefix="/api/v1/ciudadano", tags=["Portal Ciudadano (Reportes Públicos)"])
app.include_router(comunicados.router, prefix="/api/v1/comunicados", tags=["Comunicados Oficiales"])

from infrastructure.http.router import reportes
app.include_router(reportes.router, prefix="/api/v1/reportes", tags=["Reportes Técnicos Automatizados"])

@app.get("/")
def health_check():
    """Endpoint público sin autenticación para comprobar que el servidor está vivo."""
    return {"status": "Backend Operativo Online"}

if __name__ == "__main__":
    import uvicorn
    # Servidor correrá en puerto 8001 para no chocar con el ML_Service (puerto 8000)
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
