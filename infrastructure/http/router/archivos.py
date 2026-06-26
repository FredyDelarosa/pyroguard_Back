import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path

router = APIRouter()

# The container maps the root to /app, so uploads will be in /app/uploads
UPLOAD_DIR = Path("uploads")

@router.post("/upload")
async def subir_imagen(file: UploadFile = File(...)):
    """
    Sube una imagen al servidor y devuelve la URL para acceder a ella.
    Útil para reportes ciudadanos, perfiles, evidencias de campo, etc.
    """
    # Crear el directorio si no existe (por seguridad)
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    
    # Validar extensión
    extension = file.filename.split(".")[-1].lower()
    if extension not in ["jpg", "jpeg", "png", "webp"]:
        raise HTTPException(status_code=400, detail="Formato de imagen no soportado. Usa JPG, PNG o WEBP.")
    
    # Generar nombre único para evitar colisiones
    nuevo_nombre = f"{uuid.uuid4().hex}.{extension}"
    file_path = UPLOAD_DIR / nuevo_nombre
    
    try:
        # Guardar archivo en disco
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar la imagen: {str(e)}")
        
    # Devolver la URL relativa. El frontend o la base de datos la usará.
    # Como montaremos StaticFiles en /uploads, la URL pública será /uploads/nombre.jpg
    return {"url": f"/uploads/{nuevo_nombre}"}
