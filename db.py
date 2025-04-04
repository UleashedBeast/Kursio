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
            FOREIGN KEY (perfil_id) REFERENCES perfiles(id)
        )
    """)
    conn.commit()
    conn.close()

def asegurar_columna_cursada():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(materias);")
    columnas = [col[1] for col in cursor.fetchall()]

    if "cursada" not in columnas:
        print("➕ Agregando columna 'cursada' a la tabla materias...")
        cursor.execute("ALTER TABLE materias ADD COLUMN cursada TEXT;")
        conn.commit()
    else:
        print("✅ Columna 'cursada' ya existe.")
    
    conn.close()

def crear_tabla_eventos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            perfil_id INTEGER,
            fecha TEXT NOT NULL,
            tipo TEXT,
            descripcion TEXT,
            FOREIGN KEY (perfil_id) REFERENCES perfiles(id)
        );
    """)
    conn.commit()
    conn.close()
