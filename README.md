# 🎓 Kursio

**Kursio** es una aplicación en Python para el seguimiento académico de tus materias universitarias. Ideal para estudiantes que quieren organizar su cursada, registrar notas y ver su progreso de forma clara y sencilla.

---

## 🛠️ Características

- 📋 Registrar materias cursadas
- 🗓️ Guardar fechas de cursado
- 🧮 Cargar notas de parciales y finales
- ✅ Marcar estado: Aprobada, Regular, Promocionada
- 📊 Calcular promedio general
- 💾 Guardado automático en base de datos SQLite
- 🖥️ Modo consola (versión inicial)

---

## 🧩 Tecnologías utilizadas

- Python 3
- SQLite (a través de `sqlite3`)
- Estructura modular de archivos

---

## 🚀 Cómo empezar

1. 📥 Cloná el repositorio:

```bash
git clone https://github.com/tuusuario/kursio.git
cd kursio

2. 📥 Ejecuta el programa:

python main.py

Estructura de datos:

kursio/
├── main.py             # Menú principal e interacción con el usuario
├── db.py               # Gestión de la base de datos SQLite
├── materias.py         # Lógica de materias y validaciones
├── utils.py            # Funciones auxiliares
└── README.md

💡 Ideas futuras

🖼️ Interfaz gráfica con Tkinter o PyQt

📤 Exportar e importar datos en formato CSV/JSON

🧭 Modo "Plan de Carrera"

🗓️ Seguimiento por cuatrimestre/año

🌐 Versión web con Flask o FastAPI