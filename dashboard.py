import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime
import os

from perfiles import obtener_datos_perfil, obtener_id_perfil
from materias import obtener_materias_por_perfil
from editor_materias import abrir_editor_materias
from calendario import mostrar_calendario


COLORES = {
    "fondo": "#B0D1D3",
    "texto": "#1E5E73",
    "entrada": "#67B7C7",
    "boton": "#3484A1",
    "boton_texto": "#FFFFFF",
    "acento": "#D0E4E7",
    "tarjeta": "#D6EDEE"
}

def calcular_anios_cursando(anio_inicio):
    anio_actual = datetime.now().year
    return anio_actual - int(anio_inicio)

def cerrar_sesion(ventana):
    from interfaz import lanzar_selector_perfil
    ventana.destroy()
    lanzar_selector_perfil()

def mostrar_dashboard(nombre_perfil):
    perfil_id = obtener_id_perfil(nombre_perfil)
    datos = obtener_datos_perfil(nombre_perfil)
    if not datos:
        messagebox.showerror("Error", "No se pudieron obtener los datos del perfil.")
        return

    carrera, anio_inicio = datos
    anios_cursando = calcular_anios_cursando(anio_inicio)
    materias = obtener_materias_por_perfil(perfil_id)

    total_materias = len(materias)
    aprobadas = sum(1 for m in materias if m[3].lower() == "aprobada")
    promedio = 8.25  # ← por ahora simulado
    completado = int((aprobadas / total_materias) * 100) if total_materias else 0

    # === Ventana principal ===
    root = tk.Tk()
    root.title(f"Kursio - Dashboard de {nombre_perfil}")
    root.geometry("900x600")
    root.configure(bg=COLORES["fondo"])
    root.resizable(False, False)

    if os.path.exists("icono.ico"):
        root.iconbitmap("icono.ico")

    # === Panel lateral ===
    lateral = tk.Frame(root, width=200, bg=COLORES["texto"])
    lateral.pack(side="left", fill="y")

    # Imagen de perfil
    try:
        ruta_img = os.path.join("img", "avatar.jpg")
        if os.path.exists(ruta_img):
            img = Image.open(ruta_img).resize((80, 80))
            foto = ImageTk.PhotoImage(img)
            img_label = tk.Label(lateral, image=foto, bg=COLORES["texto"])
            img_label.image = foto
            img_label.pack(pady=(20, 10))
    except Exception as e:
        print("Error cargando imagen de perfil:", e)

    # Info básica
    tk.Label(lateral, text=nombre_perfil.upper(), bg=COLORES["texto"],
             fg="white", font=("Helvetica", 14, "bold")).pack(pady=(10, 5))
    tk.Label(lateral, text=f"📘 {carrera}", bg=COLORES["texto"],
             fg="white", font=("Helvetica", 10)).pack()
    tk.Label(lateral, text=f"📅 {anio_inicio}", bg=COLORES["texto"],
             fg="white", font=("Helvetica", 10)).pack()
    tk.Label(lateral, text=f"🕒 {anios_cursando} años cursando", bg=COLORES["texto"],
             fg="white", font=("Helvetica", 10)).pack(pady=(0, 20))

    botones = [
    ("🛠️ Editar materias", lambda: abrir_editor_materias(nombre_perfil)),
    ("📅 Calendario", lambda: mostrar_calendario(nombre_perfil)),
    ("⚙️ Editar perfil", lambda: messagebox.showinfo("Próximamente", "Esta sección está en desarrollo.")),
    ("🚪 Cerrar sesión", lambda: cerrar_sesion(root))
    ]

    for texto, accion in botones:
        tk.Button(lateral, text=texto, command=accion,
                  font=("Helvetica", 10), bg=COLORES["entrada"],
                  fg="black", width=20).pack(pady=5)

    # === Panel principal ===
    panel = tk.Frame(root, bg=COLORES["fondo"])
    panel.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    # Tarjetas informativas
    tarjetas = [
        ("📄 Total de materias", total_materias),
        ("✅ Aprobadas", aprobadas),
        ("⭐ Promedio", promedio),
        ("📊 Completado", f"{completado}%")
    ]

    for i, (titulo, valor) in enumerate(tarjetas):
        frame = tk.Frame(panel, bg=COLORES["tarjeta"], width=200, height=80)
        frame.grid(row=i // 2, column=i % 2, padx=20, pady=20)
        frame.grid_propagate(False)

        tk.Label(frame, text=titulo, bg=COLORES["tarjeta"],
                 fg=COLORES["texto"], font=("Helvetica", 11)).pack(pady=(10, 0))
        tk.Label(frame, text=str(valor), bg=COLORES["tarjeta"],
                 fg="black", font=("Helvetica", 20, "bold")).pack()

    # === Materias cursando ===
    materias_cursando = [m for m in materias if m[3].lower() == "cursando"]

    if materias_cursando:
        tk.Label(panel, text="📚 Materias cursando actualmente:",
                 bg=COLORES["fondo"], fg=COLORES["texto"],
                 font=("Helvetica", 13, "bold")).grid(row=2, column=0, columnspan=2, pady=(20, 5))

        for i, m in enumerate(materias_cursando):
            tk.Label(panel, text=f"• {m[0]}", bg=COLORES["fondo"],
                     fg="black", font=("Helvetica", 12), anchor="w").grid(row=3 + i, column=0, columnspan=2, sticky="w", padx=10)
    else:
        tk.Label(panel, text="📭 No estás cursando materias actualmente.",
                 bg=COLORES["fondo"], fg=COLORES["texto"],
                 font=("Helvetica", 12)).grid(row=2, column=0, columnspan=2, pady=(20, 5))

    root.mainloop()