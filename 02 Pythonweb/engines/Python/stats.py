import sqlite3
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, '../../database/clinic.db'))

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
            id TEXT,
            nombre TEXT,
            dire TEXT,
            telefono TEXT,
            edad INTEGER,
            colesterol REAL,
            glicemia REAL
        )
    ''')
    conn.commit()
    conn.close()

def fetch_all_records():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT rowid as record_number, id, nombre, dire, telefono, edad, colesterol, glicemia FROM pacientes")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def insert_record(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO pacientes (id, nombre, dire, telefono, edad, colesterol, glicemia)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('id'), data.get('nombre'), data.get('dire'),
        data.get('telefono'), data.get('edad'), data.get('colesterol'), data.get('glicemia')
    ))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id

def get_age_statistics():
    try:
        conn = get_db_connection()
        df = pd.read_sql_query("SELECT edad FROM pacientes", conn)
        conn.close()
        
        if df.empty or 'edad' not in df.columns:
            return {'min': 0, 'max': 0, 'avg': 0.0}
            
        ages = pd.to_numeric(df['edad'], errors='coerce').dropna()
        
        if ages.empty:
            return {'min': 0, 'max': 0, 'avg': 0.0}
            
        return {
            'min': int(ages.min()),
            'max': int(ages.max()),
            'avg': float(ages.mean())
        }
    except Exception as e:
        print("Error en stats:", e)
        return {'min': 0, 'max': 0, 'avg': 0.0}