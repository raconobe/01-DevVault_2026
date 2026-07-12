import json
import sqlite3
import pandas as pd
import numpy as np

def get_age_stats():
    try:
        conn = sqlite3.connect('/home/prolog/Desktop/01 DevVault_2026/01 RosettaBridge/database/clinic.db')
        # Traemos todas las columnas para verificar el nombre real
        df = pd.read_sql_query("SELECT * FROM pacientes", conn)
        conn.close()
        
        if df.empty:
            return {"min": 0, "max": 0, "avg": 0.0}
            
        # Buscamos si existe la columna de edad (ya sea 'eddad' o 'edad')
        age_col = None
        for col in df.columns:
            if col.lower() in ['eddad', 'edad']:
                age_col = col
                break
                
        if not age_col:
            return {"min": 0, "max": 0, "avg": 0.0}
            
        ages = pd.to_numeric(df[age_col], errors='coerce').dropna()
        if len(ages) == 0:
            return {"min": 0, "max": 0, "avg": 0.0}
            
        return {
            "min": int(np.min(ages)),
            "max": int(np.max(ages)),
            "avg": float(np.mean(ages))
        }
    except Exception as e:
        return {"min": 0, "max": 0, "avg": 0.0}

if __name__ == "__main__":
    print(json.dumps(get_age_stats()))