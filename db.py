# db.py
import sqlite3

def conectar():
    return sqlite3.connect("kursio.db")

def inicializar_db():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL
    )
    """)
    conn.commit()
    conn.close()