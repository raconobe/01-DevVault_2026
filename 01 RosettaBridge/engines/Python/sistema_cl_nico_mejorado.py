import sqlite3
import pandas as pd
import numpy as np
import os

# Aseguramos que la carpeta de la base de datos exista
db_folder = "database"
db_file = os.path.join(db_folder, "clinic.db")

if not os.path.exists(db_folder):
    os.makedirs(db_folder)
    print(f"Directorio '{db_folder}' creado correctamente.")

def initialize_db():
    """Crea la tabla si no existe al arrancar."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pacientes (
            record_number INTEGER PRIMARY KEY AUTOINCREMENT,
            id TEXT UNIQUE NOT NULL,
            nombre TEXT,
            dire TEXT,
            telefono TEXT,
            eddad INTEGER,
            colesterol FLOAT,
            glicemia FLOAT
        )
    """)
    conn.commit()
    conn.close()

class ClinicalAnalyzer:
    def __init__(self):
        # Conectamos con el archivo que está en la carpeta /database
        self.conn = sqlite3.connect(db_file)

    def calculate_risk_index(self):
        # Leemos los datos directamente de la base de datos
        df = pd.read_sql_query("SELECT * FROM pacientes", self.conn)
        
        if df.empty:
            return "No hay datos para procesar."

        # Cálculos usando NumPy y Pandas
        df['risk_index'] = (df['colesterol'] / 10) + (df['glicemia'] / 5)
        return df

if __name__ == "__main__":
    initialize_db()
    
    conn = sqlite3.connect(db_file)
    count = conn.execute("SELECT COUNT(*) FROM pacientes").fetchone()[0]
    if count == 0:
        conn.execute("INSERT INTO pacientes (id, nombre, eddad, colesterol, glicemia) VALUES ('A001', 'Juan Perez', 45, 220.5, 95.0)")
        conn.commit()
        print("Dato de prueba insertado.")
    conn.close()

    analyzer = ClinicalAnalyzer()
    resultado = analyzer.calculate_risk_index()
    
    print("\n--- Análisis Clínico Procesado desde Base de Datos ---")
    print(resultado[['nombre', 'eddad', 'risk_index']])   
