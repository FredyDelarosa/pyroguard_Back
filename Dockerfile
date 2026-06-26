# Usar imagen oficial ligera de Python
FROM python:3.12-slim

# Evitar que Python escriba archivos .pyc y forzar salida estándar sin buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear un usuario sin privilegios root por seguridad (CWE-250)
RUN adduser --disabled-password --gecos '' appuser

# Instalar dependencias del sistema necesarias para fpdf2 y psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

# Crear el directorio de almacenamiento local para PDFs e imágenes con permisos
RUN mkdir -p /app/storage/reportes_pdf /app/uploads && chown -R appuser:appuser /app/storage /app/uploads

# Cambiar al usuario sin privilegios
USER appuser

# Exponer el puerto interno (será enrutado por Nginx, no expuesto a internet)
EXPOSE 8001

# Comando de arranque optimizado para producción
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "4"]
