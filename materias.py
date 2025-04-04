from db import conectar

def agregar_materia(nombre, anio, departamento, estado, perfil_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO materias (nombre, anio, departamento, estado, perfil_id)
        VALUES (?, ?, ?, ?, ?)
    """, (nombre, anio, departamento, estado, perfil_id))
    conn.commit()
    conn.close()

def obtener_materias_por_perfil(perfil_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nombre, anio, departamento, estado, id, cursada
        FROM materias
        WHERE perfil_id = ?
        ORDER BY anio ASC
    """, (perfil_id,))
    materias = cursor.fetchall()
    conn.close()
    return materias

def eliminar_materia(id_materia):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM materias WHERE id = ?", (id_materia,))
    conn.commit()
    conn.close()

def agregar_materia(nombre, anio, departamento, estado, perfil_id, cursada=None):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO materias (nombre, anio, departamento, estado, perfil_id, cursada)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nombre, anio, departamento, estado, perfil_id, cursada))
    conn.commit()
    conn.close()

def actualizar_materia(id_materia, nombre, anio, departamento, estado, cursada=None):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE materias
        SET nombre = ?, anio = ?, departamento = ?, estado = ?, cursada = ?
        WHERE id = ?
    """, (nombre, anio, departamento, estado, cursada, id_materia))
    conn.commit()
    conn.close()