# usuarios.py
from db import conectar

def crear_usuario(nombre):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (nombre) VALUES (?)", (nombre,))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def usuario_existe(nombre):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE nombre = ?", (nombre,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None