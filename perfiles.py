from db import conectar

def obtener_perfiles():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM perfiles ORDER BY nombre ASC")
    perfiles = cursor.fetchall()
    conn.close()
    return perfiles

def crear_perfil(nombre):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO perfiles (nombre) VALUES (?)", (nombre,))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def actualizar_datos_perfil(nombre, carrera, anio):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE perfiles
        SET carrera = ?, anio_inicio = ?
        WHERE nombre = ?
    """, (carrera, anio, nombre))
    conn.commit()
    conn.close()