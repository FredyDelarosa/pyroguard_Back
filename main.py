from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.middleware.rate_limiter import setup_rate_limiter
from core.db.connection import engine, Base

# Importar TODOS los modelos para que SQLAlchemy (Base) los registre
from features.brigadas.infrastructure.models import BrigadaModel, BrigadistaBrigadaModel
from features.comunicados.infrastructure.models import ComunicadoModel
from features.intervenciones.infrastructure.models import IntervencionModel
from features.observaciones.infrastructure.models import ObservacionCampoModel
from features.reportes_ciudadanos.infrastructure.models import ReporteCiudadanoModel
from features.reportes_tecnicos.infrastructure.models import ReporteTecnicoModel

# Crear las tablas en la BD si no existen
Base.metadata.create_all(bind=engine)

# Importar los nuevos Routers Modulares
from features.brigadas.infrastructure.routers import router as brigadas_router
from features.comunicados.infrastructure.routers import router as comunicados_router
from features.intervenciones.infrastructure.routers import router as intervenciones_router
from features.observaciones.infrastructure.routers import router as observaciones_router
from features.reportes_ciudadanos.infrastructure.routers import router as reportes_ciudadanos_router
from features.reportes_tecnicos.infrastructure.routers import router as reportes_tecnicos_router
from core.routers import archivos

from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(
    title="PyroGuard AI - Backend Operativo (Monolito Modular)",
    description="Microservicio Core con Arquitectura Hexagonal por Features, completamente desacoplado de Auth y Crypto.",
    version="2.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

setup_rate_limiter(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar Rutas Modulares
# Para facilitar la migración del front, enrutamos todo bajo /api/v1
app.include_router(brigadas_router, prefix="/api/v1")
app.include_router(comunicados_router, prefix="/api/v1")
app.include_router(intervenciones_router, prefix="/api/v1")
app.include_router(observaciones_router, prefix="/api/v1")
app.include_router(reportes_ciudadanos_router, prefix="/api/v1")
app.include_router(reportes_tecnicos_router, prefix="/api/v1")
app.include_router(archivos.router, prefix="/api/v1/archivos", tags=["Subida de Archivos"])

os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
def health_check():
    return {"status": "Backend Operativo Modular Online"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
