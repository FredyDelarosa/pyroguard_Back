import os
from sqlalchemy import text
from core.db.connection import engine

def drop_reportes_table():
    print("Conectando a la base de datos operativa...")
    try:
        with engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS reportes_tecnicos CASCADE;"))
            conn.commit()
            print("La tabla 'reportes_tecnicos' ha sido eliminada con éxito.")
            print("Al reiniciar el contenedor de backend, SQLAlchemy la recreará con las nuevas columnas (estado, task_id).")
    except Exception as e:
        print(f"Error eliminando la tabla: {e}")

if __name__ == "__main__":
    drop_reportes_table()
