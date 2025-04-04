import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import calendar

from perfiles import obtener_id_perfil
from eventos import obtener_eventos_por_perfil, agregar_evento, actualizar_evento, eliminar_evento

COLORES = {
    "fondo": "#B0D1D3",
    "texto": "#1E5E73",
    "evento_parcial": "#FFB347",
    "evento_feriado": "#00BFFF",
    "hoy": "#FFF599",
    "fuente": "Helvetica"
}

MESES_ES = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

DIAS_ES = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]

def mostrar_calendario(nombre_perfil, anio_actual=None, mes_actual=None):
    hoy = datetime.today()
    anio_actual = anio_actual or hoy.year
    mes_actual = mes_actual or hoy.month

    perfil_id = obtener_id_perfil(nombre_perfil)
    eventos = obtener_eventos_por_perfil(perfil_id)
    eventos_por_fecha = {e[1]: (e[0], e[2], e[3]) for e in eventos}

    ventana = tk.Toplevel()
    ventana.title("📅 Calendario")
    ventana.geometry("750x660")
    ventana.configure(bg=COLORES["fondo"])

    # === CABECERA ===
    cabecera = tk.Frame(ventana, bg=COLORES["fondo"])
    cabecera.pack(pady=10)

    def cambiar_mes(delta):
        nuevo_anio = anio_actual
        nuevo_mes = mes_actual + delta
        if nuevo_mes < 1:
            nuevo_mes = 12
            nuevo_anio -= 1
        elif nuevo_mes > 12:
            nuevo_mes = 1
            nuevo_anio += 1

        # Rango de 20 años atrás/adelante
        if hoy.year - 20 <= nuevo_anio <= hoy.year + 20:
            ventana.destroy()
            mostrar_calendario(nombre_perfil, nuevo_anio, nuevo_mes)

    tk.Button(cabecera, text="◀️", command=lambda: cambiar_mes(-1),
              bg=COLORES["fondo"], fg=COLORES["texto"], font=(COLORES["fuente"], 14),
              borderwidth=0).pack(side="left", padx=10)

    tk.Label(cabecera, text=f"{MESES_ES[mes_actual]} {anio_actual}",
             font=(COLORES["fuente"], 20, "bold"),
             bg=COLORES["fondo"], fg=COLORES["texto"]).pack(side="left")

    tk.Button(cabecera, text="▶️", command=lambda: cambiar_mes(1),
              bg=COLORES["fondo"], fg=COLORES["texto"], font=(COLORES["fuente"], 14),
              borderwidth=0).pack(side="left", padx=10)

    # === ENCABEZADO DE DÍAS ===
    frame = tk.Frame(ventana, bg=COLORES["fondo"])
    frame.pack()

    for col, dia in enumerate(DIAS_ES):
        lbl = tk.Label(frame, text=dia, width=12, height=2,
                       font=(COLORES["fuente"], 12, "bold"),
                       bg=COLORES["fondo"], fg=COLORES["texto"])
        lbl.grid(row=0, column=col, padx=2, pady=5)

    # === CELDAS DEL CALENDARIO ===
    primer_dia = datetime(anio_actual, mes_actual, 1)
    _, dias_en_mes = calendar.monthrange(anio_actual, mes_actual)
    inicio_semana = (primer_dia.weekday() + 1) % 7  # lunes = 0

    fila = 1
    columna = inicio_semana
    for dia in range(1, dias_en_mes + 1):
        fecha = datetime(anio_actual, mes_actual, dia).date()
        fecha_str = fecha.isoformat()

        # Determinar color de fondo
        es_hoy = (fecha == hoy.date())
        fondo = COLORES["hoy"] if es_hoy else "white"

        celda = tk.Frame(frame, width=100, height=70, bg=fondo, bd=1, relief="solid")
        celda.grid(row=fila, column=columna, padx=3, pady=3)
        celda.grid_propagate(False)

        def handler(fecha=fecha_str):
            return lambda event: dialogo_evento(ventana, fecha, perfil_id, nombre_perfil)

        celda.bind("<Button-1>", handler())
        celda.pack_propagate(False)

        tk.Label(celda, text=str(dia), bg=fondo,
                 font=(COLORES["fuente"], 10, "bold")).pack(anchor="nw", padx=4, pady=3)

        if fecha_str in eventos_por_fecha:
            _, tipo, _ = eventos_por_fecha[fecha_str]
            color = COLORES["evento_parcial"] if tipo.lower() == "parcial" else COLORES["evento_feriado"]
            etiqueta = tk.Label(celda, text=tipo,
                                bg=color, fg="white",
                                font=(COLORES["fuente"], 9, "bold"))
            etiqueta.pack(expand=True)
        else:
            espacio = tk.Label(celda, text="", bg=fondo)
            espacio.pack(expand=True)

        columna += 1
        if columna > 6:
            columna = 0
            fila += 1

    ventana.mainloop()


def dialogo_evento(ventana_padre, fecha, perfil_id, nombre_perfil):
    from eventos import obtener_eventos_por_perfil  # prevención de ciclos
    eventos = obtener_eventos_por_perfil(perfil_id)
    eventos_por_fecha = {e[1]: (e[0], e[2], e[3]) for e in eventos}
    evento = eventos_por_fecha.get(fecha)

    win = tk.Toplevel(ventana_padre)
    win.title(f"📌 Evento para {fecha}")
    win.geometry("400x300")
    win.configure(bg=COLORES["fondo"])

    tipo_var = tk.StringVar(value=evento[1] if evento else "")
    desc_var = tk.StringVar(value=evento[2] if evento else "")

    tk.Label(win, text="Tipo de evento (ej: Parcial, Feriado)", bg=COLORES["fondo"],
             fg=COLORES["texto"], font=(COLORES["fuente"], 11)).pack(pady=10)
    tk.Entry(win, textvariable=tipo_var, font=(COLORES["fuente"], 12)).pack(pady=5)

    tk.Label(win, text="Descripción", bg=COLORES["fondo"],
             fg=COLORES["texto"], font=(COLORES["fuente"], 11)).pack(pady=10)
    tk.Entry(win, textvariable=desc_var, font=(COLORES["fuente"], 12)).pack(pady=5)

    def guardar():
        tipo = tipo_var.get().strip()
        desc = desc_var.get().strip()

        if not tipo:
            messagebox.showerror("Error", "El tipo de evento no puede estar vacío.")
            return

        if evento:
            actualizar_evento(evento[0], tipo, desc)
        else:
            agregar_evento(perfil_id, fecha, tipo, desc)

        messagebox.showinfo("Guardado", "Evento guardado correctamente.")
        win.destroy()
        ventana_padre.destroy()
        mostrar_calendario(nombre_perfil, datetime.fromisoformat(fecha).year, datetime.fromisoformat(fecha).month)

    def eliminar():
        if evento and messagebox.askyesno("Eliminar", "¿Seguro que querés borrar este evento?"):
            eliminar_evento(evento[0])
            messagebox.showinfo("Eliminado", "Evento eliminado.")
            win.destroy()
            ventana_padre.destroy()
            mostrar_calendario(nombre_perfil, datetime.fromisoformat(fecha).year, datetime.fromisoformat(fecha).month)

    tk.Button(win, text="Guardar", command=guardar,
              font=(COLORES["fuente"], 12), bg="#3484A1", fg="white").pack(pady=10)

    if evento:
        tk.Button(win, text="Eliminar", command=eliminar,
                  font=(COLORES["fuente"], 10), bg="#FF5C5C", fg="white").pack()
