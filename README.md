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

## 💡 Ideas futuras

A continuación, algunas mejoras planificadas o sugeridas para futuras versiones de **Kursio**:

### 🎨 Interfaz gráfica
- [ ] Agregar una interfaz con **Tkinter** o **PyQt**
- [ ] Permitir interacción más visual e intuitiva
- [ ] Diseño adaptable para escritorio

### 📁 Manejo de datos
- [ ] Exportar datos en **CSV** o **JSON**
- [ ] Importar datos desde archivos externos
- [ ] Backup automático de la base de datos

### 🎓 Seguimiento académico
- [ ] Agregar vista de **plan de carrera completo**
- [ ] Filtrar materias por cuatrimestre, año o estado
- [ ] Mostrar estadísticas (materias aprobadas, promedio, etc.)

### 🌐 Web / Conectividad
- [ ] Crear una versión web con **Flask** o **FastAPI**
- [ ] Permitir login de múltiples usuarios
- [ ] Sincronizar datos con la nube (opcional)

### 🛠️ Personalización y mejoras
- [ ] Soporte para materias optativas
- [ ] Personalizar estados (Ej: “En curso”, “Postergada”)
- [ ] Tema oscuro / claro en interfaz gráfica