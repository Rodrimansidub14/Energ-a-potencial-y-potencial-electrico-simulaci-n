"""
Rodrigo Mansilla 22611
Programa Parcial 2
Física 3
Simulacion de potencial eléctrico
"""


import tkinter as tk
from tkinter import ttk, Canvas, messagebox
import math
import re



animacion_en_ejecucion = False


# Constantes
EPSILON_0 = 8.854187817e-12  # Permitividad del vacío en F/m
C = 3e8  # Velocidad de la luz en m/s

# Datos de partículas conocidas
PARTICULAS = {
    'proton': {'q': 1.602e-19, 'm': 1.673e-27},
    'positron': {'q': 1.602e-19, 'm': 9.109e-31},
    'electron': {'q': 1.602e-19, 'm': 9.109e-31},
    'alfa': {'q': 3.204e-19, 'm': 6.69e-27},
    'nucleo_helio': {'q': 2 * 1.602e-19, 'm': 6.644e-27},
    'nucleo_hidrogeno': {'q': 1.602e-19, 'm': 1.673e-27},
    'nucleo_deuterio': {'q': 1.602e-19, 'm': 3.348e-27},
}

def es_notacion_cientifica(s):
    """Verifica si una cadena está en notación científica."""
    pattern = r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$'
    return re.match(pattern, s) is not None

def distancia_maxima_plano(q, sigma, m, v_i):
    return (m * v_i**2*EPSILON_0) / (q * sigma)

def distancia_maxima_esfera(q, Q, m, v_i):
    return q * Q / (2 * math.pi * EPSILON_0 * m * v_i**2)

def velocidad_escape_esfera(Q, R, m, q):
    return math.sqrt(Q * q / (2 * math.pi * EPSILON_0 * R * m))

def es_agujero_negro(Q, R, m, q):
    v_escape = velocidad_escape_esfera(Q, R, m, q)
    return v_escape >= C

def actualizar_interfaz(event):
    if tipo_carga.get() == "esfera":
        radio_label.grid()
        radio_entry.grid()
        carga_label.grid()
        carga_entry.grid()
        densidad_label.grid_remove()
        densidad_entry.grid_remove()
    else:
        radio_label.grid_remove()
        radio_entry.grid_remove()
        carga_label.grid_remove()
        carga_entry.grid_remove()
        densidad_label.grid()
        densidad_entry.grid()


def actualizar_velocidad(event):
    """Actualiza la etiqueta de velocidad basada en el porcentaje seleccionado y muestra el menú desplegable de velocidades o permite la entrada manual."""
    if velocidad_opcion.get() == "Porcentaje":
        if velocidad_combobox.get():  # Verificar si la cadena no está vacía
            porcentaje = float(velocidad_combobox.get())
            velocidad_m_s = porcentaje / 100 * C
            velocidad_label_var.set(f"Velocidad inicial: {velocidad_m_s:.3e} m/s ({porcentaje}% de c)")
        else:
            velocidad_label_var.set("Velocidad inicial:")
        velocidad_combobox.grid()
        velocidad_entry.grid_remove()
    else:
        velocidad_label_var.set("Velocidad inicial (m/s):")
        velocidad_combobox.grid_remove()
        velocidad_entry.grid()

def actualizar_particula(event):
    """Actualiza la interfaz basada en la selección de partícula."""
    if particula_opcion.get() == "Conocida":
        particula_label.grid()
        particula_combobox.grid()
        carga_label.grid_remove()
        carga_particula_entry.grid_remove()
        masa_label.grid_remove()
        masa_particula_entry.grid_remove()
    else:
        particula_label.grid_remove()
        particula_combobox.grid_remove()
        carga_label.grid()
        carga_particula_entry.grid()
        masa_label.grid()
        masa_particula_entry.grid()

def animar_particula(canvas, tipo, m, q, d_max, Q=None, R=None):
    """Animar el movimiento de la partícula."""
    global animacion_en_ejecucion
    animacion_en_ejecucion = True
    pasos = 100  # Distancia fija en píxeles para la animación
    if tipo == "esfera":
        if es_agujero_negro(Q, R, m, q):
            # Si es un agujero negro, la partícula se mueve hacia la derecha indefinidamente
            while animacion_en_ejecucion:
                canvas.move("particula", 2, 0)
                root.update()
                canvas.after(10)
        else:
            for _ in range(pasos):
                if not animacion_en_ejecucion:
                    break
                canvas.move("particula", 2, 0)
                root.update()
                canvas.after(10)
            for _ in range(pasos):
                if not animacion_en_ejecucion:
                    break
                canvas.move("particula", -2, 0)
                root.update()
                canvas.after(10)
    elif tipo == "plano":
        for _ in range(pasos):
            if not animacion_en_ejecucion:
                break
            canvas.move("particula", 2, 0)
            root.update()
            canvas.after(10)
        for _ in range(pasos):
            if not animacion_en_ejecucion:
                break
            canvas.move("particula", -2, 0)
            root.update()
            canvas.after(10)
    animacion_en_ejecucion = False



def iniciar_simulacion():
    global animacion_en_ejecucion
    animacion_en_ejecucion = False
    tipo = tipo_carga.get()
    
    # Obtener y validar la velocidad inicial
    if velocidad_opcion.get() == "Porcentaje":
        porcentaje = float(velocidad_combobox.get())
        velocidad_inicial = porcentaje / 100 * C
    else:
        velocidad_str = velocidad_entry.get()
        if not es_notacion_cientifica(velocidad_str):
            messagebox.showerror("Error", "Por favor, ingrese una velocidad válida.")
            return
        velocidad_inicial = float(velocidad_str)

    if velocidad_inicial >= C:
        messagebox.showerror("Error", "La velocidad no puede superar la velocidad de la luz.")
        return
    # Obtener la carga y masa de la partícula
    if particula_opcion.get() == "Conocida":
        particula_seleccionada = particula_combobox.get()
        q = PARTICULAS[particula_seleccionada]['q']
        m = PARTICULAS[particula_seleccionada]['m']
    else:
        q = float(carga_particula_entry.get())
        m = float(masa_particula_entry.get())

    Q = None
    R = None
    if tipo == "esfera":
        R = float(radio_entry.get())
        Q = float(carga_entry.get())
        d_max = distancia_maxima_esfera(q, Q, m, velocidad_inicial)
        v_escape = velocidad_escape_esfera(Q, R, m, q)
        if es_agujero_negro(Q, R, m, q):
            resultado = f"Distancia máxima de alejamiento: {d_max:.3e} metros\n" \
                        f"Velocidad de escape: {v_escape:.3e} m/s\n" \
                        "La esfera se ha convertido en un agujero negro electrostático."
        else:
            resultado = f"Distancia máxima de alejamiento: {d_max:.3e} metros\n" \
                        f"Velocidad de escape: {v_escape:.3e} m/s"
    else:
        sigma = float(densidad_entry.get())
        d_max = distancia_maxima_plano(q, sigma, m, velocidad_inicial)
        resultado = f"Distancia máxima de alejamiento: {d_max:.3e} metros"

    # Muestra los resultados en el widget Text
    resultados_text.config(state=tk.NORMAL)  # Habilita la edición temporalmente
    resultados_text.delete(1.0, tk.END)  # Limpia el contenido anterior
    resultados_text.insert(tk.END, resultado)  # Inserta los nuevos resultados
    resultados_text.config(state=tk.DISABLED)  # Deshabilita la edición para hacerlo de solo lectura

    # Animación
    canvas.delete("all")
    if tipo == "esfera":
        canvas.create_oval(0, 125, 150, 275, fill="blue")  # Esfera
        canvas.create_oval(145, 195, 155, 205, fill="red", tags="particula")  # Partícula en posición inicial en el eje de simetría horizontal de la esfera
    else:
       canvas.create_rectangle(0, 75, 25, 225, fill="blue", tags="plano")
       canvas.create_oval(25, 145, 35, 155, fill="red", tags="particula")  # Partícula en posición inicial en la superficie del plano

    animar_particula(canvas, tipo, m, q, d_max, Q, R)

root = tk.Tk()
root.title("Simulación de partícula en campo eléctrico")

# Seleccionar tipo de carga
tipo_carga_label = ttk.Label(root, text="Tipo de carga:")
tipo_carga_label.grid(row=0, column=0, padx=10, pady=10)
tipo_carga = ttk.Combobox(root, values=["esfera", "plano"])
tipo_carga.grid(row=0, column=1, padx=10, pady=10)
tipo_carga.bind("<<ComboboxSelected>>", actualizar_interfaz)

# Entradas para esfera
radio_label = ttk.Label(root, text="Radio de la esfera (m):")
radio_label.grid(row=1, column=0, padx=10, pady=10)
radio_entry = ttk.Entry(root)
radio_entry.grid(row=1, column=1, padx=10, pady=10)

carga_label = ttk.Label(root, text="Carga total de la esfera (C):")
carga_label.grid(row=2, column=0, padx=10, pady=10)
carga_entry = ttk.Entry(root)
carga_entry.grid(row=2, column=1, padx=10, pady=10)

# Entrada para plano
densidad_label = ttk.Label(root, text="Densidad superficial de carga (C/m^2):")
densidad_label.grid(row=3, column=0, padx=10, pady=10)
densidad_entry = ttk.Entry(root)
densidad_entry.grid(row=3, column=1, padx=10, pady=10)

# Seleccionar partícula o ingresar valores
particula_opcion_label = ttk.Label(root, text="Opción de partícula:")
particula_opcion_label.grid(row=4, column=0, padx=10, pady=10)
particula_opcion = ttk.Combobox(root, values=["Conocida", "Ingresar valores"])
particula_opcion.grid(row=4, column=1, padx=10, pady=10)
particula_opcion.bind("<<ComboboxSelected>>", actualizar_particula)

# Seleccionar partícula conocida
particula_label = ttk.Label(root, text="Partícula:")
particula_label.grid(row=5, column=0, padx=10, pady=10)
particula_combobox = ttk.Combobox(root, values=list(PARTICULAS.keys()))
particula_combobox.grid(row=5, column=1, padx=10, pady=10)

# Ingresar carga y masa de la partícula
carga_label = ttk.Label(root, text="Carga de la partícula (C):")
carga_label.grid(row=6, column=0, padx=10, pady=10)
carga_particula_entry = ttk.Entry(root)
carga_particula_entry.grid(row=6, column=1, padx=10, pady=10)

masa_label = ttk.Label(root, text="Masa de la partícula (kg):")
masa_label.grid(row=7, column=0, padx=10, pady=10)
masa_particula_entry = ttk.Entry(root)
masa_particula_entry.grid(row=7, column=1, padx=10, pady=10)


# Seleccionar velocidad inicial
velocidad_opcion_label = ttk.Label(root, text="Tipo de velocidad:")
velocidad_opcion_label.grid(row=8, column=0, padx=10, pady=10)
velocidad_opcion = ttk.Combobox(root, values=["Porcentaje", "Valor absoluto"])
velocidad_opcion.grid(row=8, column=1, padx=10, pady=10)
velocidad_opcion.set("Porcentaje")
velocidad_opcion.bind("<<ComboboxSelected>>", actualizar_velocidad)

velocidad_label_var = tk.StringVar()
velocidad_label_var.set("Velocidad inicial:")
velocidad_label = ttk.Label(root, textvariable=velocidad_label_var)
velocidad_label.grid(row=9, column=0, padx=10, pady=10)
velocidad_combobox = ttk.Combobox(root, values=[1, 5, 10, 50, 75, 90, 95, 99])
velocidad_combobox.grid(row=9, column=1, padx=10, pady=10)
velocidad_combobox.bind("<<ComboboxSelected>>", actualizar_velocidad)

velocidad_entry = ttk.Entry(root)
velocidad_entry.grid(row=9, column=1, padx=10, pady=10)
velocidad_entry.grid_remove()  # Ocultar inicialmente

# Botón para iniciar simulación
simular_btn = ttk.Button(root, text="Simular", command=iniciar_simulacion)
simular_btn.grid(row=10, column=0, columnspan=2, pady=20)

# Canvas para la animación
canvas = Canvas(root, width=300, height=300)
canvas.grid(row=11, column=0, columnspan=2, padx=10, pady=10)

# Widget para mostrar los resultados
resultados_text = tk.Text(root, height=6, width=50, wrap=tk.WORD, state=tk.DISABLED)
resultados_text.grid(row=12, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
