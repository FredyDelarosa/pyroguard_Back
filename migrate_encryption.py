import logging
import sys

# Ajustar path si es necesario para imports
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.db.connection import SessionLocal
from infrastructure.database.postgres.models import Usuario, ReporteCiudadano
from core.security import persistence_interceptor

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("MigracionCifrado")

def migrate_usuarios(db):
    logger.info("Buscando usuarios no cifrados...")
    usuarios = db.query(Usuario).all()
    migrated_count = 0
    
    for usuario in usuarios:
        # Verificamos si el campo marcado como sensible no está ya cifrado
        if usuario.nombre and not usuario.nombre.startswith("enc::v1::"):
            persistence_interceptor.prepare_for_write(usuario)
            migrated_count += 1
    
    if migrated_count > 0:
        db.commit()
    logger.info(f"Se encriptaron {migrated_count} registros de la tabla 'usuarios'.")

def migrate_reportes(db):
    logger.info("Buscando reportes ciudadanos no cifrados...")
    reportes = db.query(ReporteCiudadano).all()
    migrated_count = 0
    
    for reporte in reportes:
        # Verificamos si el campo marcado como sensible no está ya cifrado
        if reporte.descripcion and not reporte.descripcion.startswith("enc::v1::"):
            persistence_interceptor.prepare_for_write(reporte)
            migrated_count += 1
            
    if migrated_count > 0:
        db.commit()
    logger.info(f"Se encriptaron {migrated_count} registros de la tabla 'reportes_ciudadanos'.")

def run_migration():
    db = SessionLocal()
    try:
        logger.info("Iniciando el proceso de cifrado de base de datos...")
        migrate_usuarios(db)
        migrate_reportes(db)
        logger.info("¡Migración completada exitosamente! Todos los datos en reposo están seguros.")
    except Exception as e:
        logger.error(f"Ocurrió un error inesperado durante la migración: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    run_migration()
