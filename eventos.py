from db import conectar

def obtener_eventos_por_perfil(perfil_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, fecha, tipo, descripcion FROM eventos WHERE perfil_id = ?", (perfil_id,))
    eventos = cursor.fetchall()
    conn.close()
    return eventos

def agregar_evento(perfil_id, fecha, tipo, descripcion):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO eventos (perfil_id, fecha, tipo, descripcion) VALUES (?, ?, ?, ?)",
                   (perfil_id, fecha, tipo, descripcion))
    conn.commit()
    conn.close()

def actualizar_evento(evento_id, tipo, descripcion):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE eventos SET tipo = ?, descripcion = ? WHERE id = ?",
                   (tipo, descripcion, evento_id))
    conn.commit()
    conn.close()

def eliminar_evento(evento_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM eventos WHERE id = ?", (evento_id,))
    conn.commit()
    conn.close()