import tkinter as tk
from tkinter import messagebox
from perfiles import obtener_perfiles, crear_perfil, perfil_incompleto, eliminar_perfil
from guia_inicial import mostrar_guia
from dashboard import mostrar_dashboard
import os

# 🎨 Paleta de colores personalizada
COLORES = {
    "fondo": "#B0D1D3",
    "texto": "#1E5E73",
    "entrada": "#67B7C7",
    "boton": "#3484A1",
    "boton_texto": "#FFFFFF",
    "acento": "#D0E4E7"
}

def lanzar_selector_perfil():
    def seleccionar_perfil(nombre):
        ventana.destroy()
        if perfil_incompleto(nombre):
            messagebox.showinfo("🔄 Completar perfil", f"Faltan datos en el perfil '{nombre}'. Vamos a completarlos.")
            mostrar_guia(nombre)
        else:
            mostrar_dashboard(nombre)

    def mostrar_creador_perfil():
        for widget in contenedor.winfo_children():
            widget.destroy()

        tk.Label(contenedor, text="🆕 Crear nuevo perfil",
                 font=("Helvetica", 16),
                 bg=COLORES["fondo"], fg=COLORES["texto"]).pack(pady=10)

        entry = tk.Entry(contenedor, font=("Helvetica", 12),
                         bg=COLORES["entrada"], width=30)
        entry.pack(pady=5)

        def crear():
            nombre = entry.get().strip()
            if nombre and crear_perfil(nombre):
                ventana.destroy()
                mostrar_guia(nombre)
            else:
                messagebox.showerror("❌ Error", "Ese perfil ya existe o el nombre es inválido.")

        tk.Button(contenedor, text="Crear perfil", command=crear,
                  font=("Helvetica", 12),
                  bg=COLORES["boton"], fg=COLORES["boton_texto"],
                  width=15).pack(pady=10)

        tk.Button(contenedor, text="Volver", command=lanzar_selector_perfil,
                  font=("Helvetica", 10),
                  bg=COLORES["fondo"], fg=COLORES["texto"],
                  relief="flat").pack(pady=5)

    def confirmar_eliminacion(nombre):
        if messagebox.askyesno("Eliminar perfil", f"¿Estás seguro de que querés borrar el perfil '{nombre}'? Esta acción no se puede deshacer."):
            eliminar_perfil(nombre)
            messagebox.showinfo("Perfil eliminado", f"🗑️ Perfil '{nombre}' eliminado.")
            construir_lista_perfiles()

    def construir_lista_perfiles():
        for widget in contenedor.winfo_children():
            widget.destroy()

        perfiles = obtener_perfiles()
        if not perfiles:
            mostrar_creador_perfil()
            return

        tk.Label(contenedor, text="👤 Seleccioná tu perfil",
                 font=("Helvetica", 16),
                 bg=COLORES["fondo"], fg=COLORES["texto"]).pack(pady=10)

        nombres = [perfil[1] for perfil in perfiles]
        seleccion = tk.StringVar()
        seleccion.set(nombres[0])

        menu = tk.OptionMenu(contenedor, seleccion, *nombres)
        menu.config(font=("Helvetica", 12),
                    bg=COLORES["entrada"], fg="black", width=25)
        menu.pack(pady=10)

        tk.Button(contenedor, text="Ingresar",
                  command=lambda: seleccionar_perfil(seleccion.get()),
                  font=("Helvetica", 12),
                  bg=COLORES["boton"], fg=COLORES["boton_texto"],
                  width=15).pack(pady=5)

        tk.Button(contenedor, text="🗑️ Eliminar perfil",
                  command=lambda: confirmar_eliminacion(seleccion.get()),
                  font=("Helvetica", 11),
                  bg="#FF5C5C", fg="white",
                  width=15).pack(pady=5)

        tk.Button(contenedor, text="Crear nuevo perfil",
                  command=mostrar_creador_perfil,
                  font=("Helvetica", 11),
                  bg=COLORES["acento"], fg=COLORES["texto"],
                  relief="flat").pack(pady=20)

    # 🪟 Ventana principal
    ventana = tk.Tk()
    ventana.title("Kursio - Selección de perfil")
    ventana.geometry("800x600")
    ventana.resizable(False, False)
    ventana.configure(bg=COLORES["fondo"])

    # Icono si existe
    icono_path = os.path.join(os.path.dirname(__file__), "icono.ico")
    if os.path.exists(icono_path):
        ventana.iconbitmap(icono_path)

    contenedor = tk.Frame(ventana, bg=COLORES["fondo"])
    contenedor.pack(expand=True)

    construir_lista_perfiles()
    ventana.mainloop()