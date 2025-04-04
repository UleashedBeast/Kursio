def crear_tabla_materias():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS materias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            anio INTEGER,
            departamento TEXT,
            estado TEXT,
            perfil_id INTEGER,
            cursada TEXT,
            FOREIGN KEY (perfil_id) REFERENCES perfiles(id)
        )
    """)
    conn.commit()
    conn.close()