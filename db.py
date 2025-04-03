import sqlite3

def conectar():
    return sqlite3.connect("kursio.db")

def inicializar_db():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS perfiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL,
        carrera TEXT,
        anio_inicio INTEGER
    )
    """)
    conn.commit()
    conn.close()