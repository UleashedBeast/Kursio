# main.py
from db import inicializar_db
from interfaz import lanzar_login

if __name__ == "__main__":
    inicializar_db()
    lanzar_login()
