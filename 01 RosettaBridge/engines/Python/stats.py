import sqlite3
import pandas as pd
import numpy as np

def get_age_stats():
    conn = sqlite3.connect('database/clinic.db')
    # Unificado a la tabla 'pacientes'
    df = pd.read_sql_query("SELECT eddad FROM pacientes", conn)
    conn.close()
    
    if df.empty:
        return {"min": 0, "max": 0, "avg": 0}
        
    ages = df['eddad'].values
    return {
        "min": int(np.min(ages)),
        "max": int(np.max(ages)),
        "avg": float(np.mean(ages))
    }
     
     
if __name__ == "__main__":
    print(get_age_stats())