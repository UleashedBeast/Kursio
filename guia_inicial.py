import tkinter as tk
from tkinter import messagebox
from perfiles import actualizar_datos_perfil
import os

COLORES = {
    "fondo": "#B0D1D3",
    "texto": "#1E5E73",
    "entrada": "#67B7C7",
    "boton": "#3484A1",
    "boton_texto": "#FFFFFF"
}

def mostrar_guia(nombre_perfil):
    datos = {
        "carrera": "",
        "anio_inicio": ""
    }
    paso = [0]
    entrada = [None]  # Lo manejamos como lista para modificar dentro de funciones

    ventana = tk.Tk()
    ventana.title("Kursio - Configuración inicial")
    ventana.geometry("800x600")
    ventana.configure(bg=COLORES["fondo"])
    ventana.resizable(False, False)

    if os.path.exists("icono.ico"):
        ventana.iconbitmap("icono.ico")

    contenedor = tk.Frame(ventana, bg=COLORES["fondo"])
    contenedor.pack(expand=True)

    def siguiente():
        valor = entrada[0].get().strip()
        if paso[0] == 0:
            if not valor:
                messagebox.showerror("⚠️ Error", "Por favor ingresá tu carrera.")
                return
            datos["carrera"] = valor
            paso[0] += 1
            mostrar_paso()

        elif paso[0] == 1:
            if not valor.isdigit():
                messagebox.showerror("⚠️ Error", "El año de inicio debe ser un número.")
                return
            datos["anio_inicio"] = int(valor)
            actualizar_datos_perfil(nombre_perfil, datos["carrera"], datos["anio_inicio"])
            messagebox.showinfo("✅ ¡Listo!", f"Perfil '{nombre_perfil}' configurado con éxito.\n🎓 Carrera: {datos['carrera']}\n📅 Año: {datos['anio_inicio']}")
            ventana.destroy()

    def mostrar_paso():
        for widget in contenedor.winfo_children():
            widget.destroy()

        if paso[0] == 0:
            tk.Label(contenedor, text=f"👋 ¡Hola {nombre_perfil}!\nVamos a configurar tu perfil.",
                     font=("Helvetica", 16), bg=COLORES["fondo"],
                     fg=COLORES["texto"], justify="center").pack(pady=30)

            tk.Label(contenedor, text="📘 ¿Qué carrera estás estudiando?",
                     font=("Helvetica", 18), bg=COLORES["fondo"],
                     fg=COLORES["texto"]).pack(pady=10)

            entrada[0] = tk.Entry(contenedor, font=("Helvetica", 14),
                                  bg=COLORES["entrada"], width=40)
            entrada[0].pack(pady=10)

        elif paso[0] == 1:
            tk.Label(contenedor, text="📅 ¿En qué año comenzaste la carrera?",
                     font=("Helvetica", 18), bg=COLORES["fondo"],
                     fg=COLORES["texto"]).pack(pady=40)

            entrada[0] = tk.Entry(contenedor, font=("Helvetica", 14),
                                  bg=COLORES["entrada"], width=20)
            entrada[0].pack(pady=10)

        tk.Button(contenedor, text="Siguiente ➡️", command=siguiente,
                  font=("Helvetica", 12), bg=COLORES["boton"],
                  fg=COLORES["boton_texto"], width=15).pack(pady=30)

    mostrar_paso()
    ventana.mainloop()