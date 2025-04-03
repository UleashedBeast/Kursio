import tkinter as tk
from tkinter import messagebox
from usuarios import usuario_existe, crear_usuario
import os

# 🎨 Paleta basada en la imagen subida
COLORES = {
    "fondo": "#B0D1D3",           # fondo general
    "texto": "#1E5E73",           # texto y títulos
    "entrada": "#67B7C7",         # fondo de los campos de texto
    "boton": "#3484A1",           # botones
    "boton_texto": "#FFFFFF",     # texto sobre los botones
    "acento": "#D0E4E7"           # detalles suaves o hover
}

def lanzar_login():
    def ingresar():
        nombre = entry_usuario.get().strip()
        if usuario_existe(nombre):
            messagebox.showinfo("Bienvenido", f"Hola {nombre}, accediste correctamente.")
            # Acá cargarías la siguiente pantalla
        else:
            messagebox.showerror("Error", "El usuario no existe.")

    def registrar():
        nombre = entry_usuario.get().strip()
        if crear_usuario(nombre):
            messagebox.showinfo("Usuario creado", f"Usuario '{nombre}' creado con éxito.")
        else:
            messagebox.showerror("Error", "Ese nombre de usuario ya existe.")

    # Crear ventana
    ventana = tk.Tk()
    ventana.title("Kursio - Ingreso")
    ventana.geometry("800x600")
    ventana.resizable(False, False)
    ventana.configure(bg=COLORES["fondo"])

    # Icono (si lo tenés como `icono.ico`)
    icono_path = os.path.join(os.path.dirname(__file__), "icono.ico")
    if os.path.exists(icono_path):
        ventana.iconbitmap(icono_path)

    # Widgets
    tk.Label(
        ventana, text="Bienvenido a Kursio",
        font=("Helvetica", 24, "bold"),
        bg=COLORES["fondo"], fg=COLORES["texto"]
    ).pack(pady=40)

    tk.Label(
        ventana, text="Ingrese su nombre de usuario",
        font=("Helvetica", 14),
        bg=COLORES["fondo"], fg=COLORES["texto"]
    ).pack(pady=10)

    entry_usuario = tk.Entry(
        ventana,
        font=("Helvetica", 12),
        width=30,
        bg=COLORES["entrada"],
        fg="black",
        relief="flat",
        highlightthickness=2,
        highlightbackground=COLORES["texto"]
    )
    entry_usuario.pack(pady=10)

    # Botón Ingresar
    tk.Button(
        ventana, text="Ingresar",
        font=("Helvetica", 12, "bold"),
        width=15,
        bg=COLORES["boton"],
        fg=COLORES["boton_texto"],
        relief="flat",
        command=ingresar
    ).pack(pady=15)

    # Botón Crear usuario
    tk.Button(
        ventana, text="Crear usuario",
        font=("Helvetica", 12),
        width=15,
        bg=COLORES["boton"],
        fg=COLORES["boton_texto"],
        relief="flat",
        command=registrar
    ).pack(pady=5)

    ventana.mainloop()