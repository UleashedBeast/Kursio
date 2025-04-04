from db import inicializar_db, crear_tabla_materias, asegurar_columna_cursada
from interfaz import lanzar_selector_perfil
from db import crear_tabla_eventos

inicializar_db()
crear_tabla_materias()
asegurar_columna_cursada()
lanzar_selector_perfil()
crear_tabla_eventos()
