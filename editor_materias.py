import tkinter as tk
from tkinter import messagebox
from materias import obtener_materias_por_perfil, agregar_materia, eliminar_materia, actualizar_materia
from perfiles import obtener_id_perfil
from db import conectar

COLORES = {
    "fondo": "#B0D1D3",
    "texto": "#1E5E73",
    "entrada": "#67B7C7",
    "boton": "#3484A1",
    "boton_texto": "#FFFFFF"
}

DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

def abrir_editor_materias(nombre_perfil):
    perfil_id = obtener_id_perfil(nombre_perfil)
    materias = obtener_materias_por_perfil(perfil_id)

    ventana = tk.Toplevel()
    ventana.title("Editar materias")
    ventana.geometry("700x600")
    ventana.configure(bg=COLORES["fondo"])
    ventana.resizable(False, False)

    tk.Label(ventana, text=f"Materias de {nombre_perfil}", font=("Helvetica", 16, "bold"),
             bg=COLORES["fondo"], fg=COLORES["texto"]).pack(pady=20)

    if not materias:
        tk.Label(ventana, text="📭 No hay materias cargadas aún.",
                 bg=COLORES["fondo"], fg=COLORES["texto"],
                 font=("Helvetica", 12)).pack(pady=10)

    for materia in materias:
        nombre, anio, depto, estado, id_materia, cursada = materia
        frame = tk.Frame(ventana, bg=COLORES["fondo"])
        frame.pack(pady=5)

        info = f"{nombre} ({anio}° año, {depto}) - Estado: {estado}"
        tk.Label(frame, text=info, bg=COLORES["fondo"], fg=COLORES["texto"],
                 font=("Helvetica", 12), width=50, anchor="w").pack(side="left", padx=10)

        tk.Button(frame, text="Editar", command=lambda idm=id_materia: editar_materia(idm, perfil_id, ventana, nombre_perfil),
                  font=("Helvetica", 10), bg=COLORES["entrada"]).pack(side="left", padx=5)

        tk.Button(frame, text="Eliminar", command=lambda idm=id_materia: eliminar(idm, ventana, perfil_id, nombre_perfil),
                  font=("Helvetica", 10), bg="#FF5C5C", fg="white").pack(side="left", padx=5)

    tk.Button(ventana, text="➕ Agregar nueva materia",
              command=lambda: editar_materia(None, perfil_id, ventana, nombre_perfil),
              bg=COLORES["boton"], fg=COLORES["boton_texto"],
              font=("Helvetica", 12)).pack(pady=30)

def editar_materia(id_materia, perfil_id, padre, nombre_perfil):
    ventana = tk.Toplevel(padre)
    ventana.title("Editar materia" if id_materia else "Agregar materia")
    ventana.geometry("500x600")
    ventana.configure(bg=COLORES["fondo"])

    campos = ["Nombre", "Año", "Departamento", "Estado"]
    entradas = {}

    valores = {}
    cursada_valor = ""
    if id_materia:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, anio, departamento, estado, cursada FROM materias WHERE id = ?", (id_materia,))
        resultado = cursor.fetchone()
        conn.close()
        if resultado:
            valores = dict(zip(campos, resultado[:-1]))
            cursada_valor = resultado[-1] or ""

    for campo in campos:
        tk.Label(ventana, text=campo, font=("Helvetica", 12),
                 bg=COLORES["fondo"], fg=COLORES["texto"]).pack(pady=5)
        entry = tk.Entry(ventana, font=("Helvetica", 12), width=30, bg=COLORES["entrada"])
        entry.pack()
        if campo in valores:
            entry.insert(0, str(valores[campo]))
        entradas[campo] = entry

    # === Cursada por día (desde-hasta) ===
    tk.Label(ventana, text="🗓️ Días y horarios de cursada", font=("Helvetica", 13, "bold"),
             bg=COLORES["fondo"], fg=COLORES["texto"]).pack(pady=10)

    dias_seleccionados = {}
    entradas_hora_desde = {}
    entradas_hora_hasta = {}

    # Parsear horarios guardados (ej: Lunes 18:00-20:00)
    dias_previos = {}
    for bloque in cursada_valor.split(";"):
        if bloque.strip():
            try:
                partes = bloque.strip().split(" ")
                dia = partes[0]
                horas = partes[1].split("-")
                dias_previos[dia] = (horas[0], horas[1])
            except:
                pass

    for dia in DIAS_SEMANA:
        frame_dia = tk.Frame(ventana, bg=COLORES["fondo"])
        frame_dia.pack(pady=3)

        var = tk.BooleanVar(value=dia in dias_previos)
        chk = tk.Checkbutton(frame_dia, text=dia, variable=var,
                             bg=COLORES["fondo"], fg=COLORES["texto"],
                             font=("Helvetica", 11))
        chk.pack(side="left", padx=5)
        dias_seleccionados[dia] = var

        tk.Label(frame_dia, text="Desde:", bg=COLORES["fondo"],
                 fg=COLORES["texto"]).pack(side="left", padx=(5, 2))
        entrada_desde = tk.Entry(frame_dia, font=("Helvetica", 10), width=6, bg=COLORES["entrada"])
        entrada_desde.pack(side="left")
        entradas_hora_desde[dia] = entrada_desde

        tk.Label(frame_dia, text="Hasta:", bg=COLORES["fondo"],
                 fg=COLORES["texto"]).pack(side="left", padx=(5, 2))
        entrada_hasta = tk.Entry(frame_dia, font=("Helvetica", 10), width=6, bg=COLORES["entrada"])
        entrada_hasta.pack(side="left")
        entradas_hora_hasta[dia] = entrada_hasta

        if dia in dias_previos:
            entrada_desde.insert(0, dias_previos[dia][0])
            entrada_hasta.insert(0, dias_previos[dia][1])


    def guardar():
        nombre = entradas["Nombre"].get().strip()
        anio = entradas["Año"].get().strip()
        depto = entradas["Departamento"].get().strip()
        estado = entradas["Estado"].get().strip()

        if not (nombre and anio.isdigit() and depto and estado):
            messagebox.showerror("Error", "Todos los campos son obligatorios y el año debe ser numérico.")
            return

        # Armar el string de cursada
        bloques = []
        for dia in DIAS_SEMANA:
            if dias_seleccionados[dia].get():
                desde = entradas_hora_desde[dia].get().strip()
                hasta = entradas_hora_hasta[dia].get().strip()

                if not (desde and hasta and ":" in desde and ":" in hasta and len(desde) == 5 and len(hasta) == 5):
                    messagebox.showerror("Formato incorrecto", f"Verificá los horarios para {dia} (formato HH:MM).")
                    return

                bloques.append(f"{dia} {desde}-{hasta}")

        cursada_final = "; ".join(bloques)


        if id_materia:
            actualizar_materia(id_materia, nombre, int(anio), depto, estado, cursada_final)
            messagebox.showinfo("✅ Actualizado", "Materia actualizada correctamente.")
        else:
            agregar_materia(nombre, int(anio), depto, estado, perfil_id, cursada_final)
            messagebox.showinfo("✅ Agregado", "Materia agregada correctamente.")

        ventana.destroy()
        padre.destroy()
        abrir_editor_materias(nombre_perfil)

    tk.Button(ventana, text="Guardar", command=guardar,
              font=("Helvetica", 12),
              bg=COLORES["boton"], fg=COLORES["boton_texto"]).pack(pady=30)

def eliminar(id_materia, ventana, perfil_id, nombre_perfil):
    if messagebox.askyesno("Eliminar", "¿Estás seguro de que querés eliminar esta materia?"):
        eliminar_materia(id_materia)
        ventana.destroy()
        abrir_editor_materias(nombre_perfil)