import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, savgol_filter

# Inicializar listas para guardar resultados
x_minimos = []
r_values = []
n_values = []


dx=0.002
ro=33.06612
# Constante N
N = 415.52079

# Ruta base
base_path = "NA/g_rs"
atomtype = base_path.split("/")[0]

out_folder= f"{atomtype}-OW"
if not os.path.exists(out_folder):
    os.makedirs(out_folder)

# Recorrer todas las carpetas en la ruta base
for folder in os.listdir(base_path):
    folder_path = os.path.join(base_path, folder)
    
    # Verificar si el nombre de la carpeta tiene el formato N1-N2 y contiene un archivo gr.xvg
    if os.path.isdir(folder_path) and "-" in folder:
        try:
            # Extraer N1 y N2 del nombre de la carpeta
            n1, n2 = map(float, folder.split("-"))
            r = (n1 + n2) / 2  # Calcular r
            r_values.append(r)

            # Ruta del archivo gr.xvg
            file_path = os.path.join(folder_path, "gr.xvg")
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Archivo 'gr.xvg' no encontrado en {folder_path}")
            
            # Cargar datos del archivo gr.xvg
            data = np.loadtxt(file_path, comments=["@", "#"])  # Ignorar líneas de encabezado
            x = data[:, 0]
            y = data[:, 1]

            # Suavizar la curva para reducir el ruido
            y_suave = savgol_filter(y, window_length=20, polyorder=3)

            # Encontrar los picos en la curva suavizada
            peaks, _ = find_peaks(y_suave, height=0.5)  # Cambia el umbral de "height" según sea necesario
            
            # Determinar los dos primeros máximos significativos
            if len(peaks) < 2:
                raise ValueError(f"No se encontraron dos máximos significativos en {file_path}")
            maximos = peaks[:2]

            # Encontrar el mínimo en la curva original entre los dos máximos identificados
            inicio, fin = maximos[0], maximos[1]
            min_index = np.argmin(y[inicio:fin]) + inicio
            x_min = x[min_index]
            y_min = y[min_index]
            x_minimos.append(x_min)

            # Calcular el valor de la columna adicional
            sumatoria = np.sum(x[:min_index + 1]**2 * y[:min_index + 1] * dx)  # Suma hasta x_min
            n_value = N * sumatoria
            
            # Graficar
            plt.axhline(y=1, color="black", linestyle="--", alpha=0.5, linewidth=0.5)
            plt.plot(x, y, label="Distribución Radial", alpha=0.5, linewidth=3)
            plt.plot(x, y_suave, label="Datos suavizados", linewidth=1, color="red")
            plt.axvline(x=x_min, color="purple", alpha=0.7, linestyle="--", label="Primera capa de solvatación")
            plt.plot(x_min, y_min, "o", alpha=0.8, label=f"Mínimo (curva original) en r= {x_min:.4f} nm", color="orange")
            
            # Agregar texto en el margen superior izquierdo
            plt.text(
                0.50,  # Coordenada x en espacio relativo (0: izquierda, 1: derecha)
                0.45,  # Coordenada y en espacio relativo (0: abajo, 1: arriba)
                rf"$cn_{{\mathrm{{OW}}}} = {n_value:.4f}$",  # Texto con el valor de n_value
                fontsize=12,  # Tamaño de la fuente
                color="black",  # Color del texto
                ha="left",  # Alineación horizontal
                va="top",  # Alineación vertical
                transform=plt.gca().transAxes,  # Usar coordenadas relativas al eje
            )
            
            plt.text(
            0.50,  # Coordenada x relativa
            0.55,  # Coordenada y relativa, un poco más arriba
            rf"$\rho_{{\mathrm{{SPCE}}}} = {ro:.4f} \; SPCE/nm^{{3}}$",  # Texto con formato LaTeX
            fontsize=12,  # Tamaño de letra
            color="black",  # Color
            ha="left",  # Alineación horizontal
            va="top",  # Alineación vertical
            transform=plt.gca().transAxes,  # Coordenadas relativas
        )
            
            plt.legend()
            plt.xlabel("r (nm)")
            plt.ylabel("g(r)")
            plt.title(f"{atomtype}-OW-{r:.2f}")
            plt.savefig(f"{out_folder}/{atomtype}-OW-{r:.2f}.svg")
            plt.close()

            
            n_values.append(n_value)

        except Exception as e:
            print(f"Error procesando {folder_path}: {e}")

# Ordenar los resultados por r
resultados_ordenados = sorted(zip(r_values, x_minimos, n_values))

# Descomponer los valores de resultados_ordenados
r_values = [row[0] for row in resultados_ordenados]
x_minimos = [row[1] for row in resultados_ordenados]
n_values = [row[2] for row in resultados_ordenados]

# Crear la figura y un eje con escalas diferentes
fig, ax1 = plt.subplots()

# Eje izquierdo para x_minimos
ax1.plot(r_values, x_minimos, label="x_min", color="blue", linewidth=2)
ax1.set_xlabel("r (nm)")
ax1.set_ylabel("x_min", color="blue")
ax1.tick_params(axis='y', labelcolor="blue")

# Crear un segundo eje para N usando el mismo eje x
ax2 = ax1.twinx()
ax2.plot(r_values, n_values, label="N", color="red", linewidth=2, linestyle="--")
ax2.set_ylabel("N", color="red")
ax2.tick_params(axis='y', labelcolor="red")

# Título y leyenda
plt.title("x_min y N en función de r")
fig.tight_layout()
fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))  # Coloca la leyenda adecuadamente
plt.savefig(f"{out_folder}/x_min_N_vs_r.svg")
plt.close()

# Guardar resultados en el archivo cn.xvg
output_path = f"{out_folder}/cn{atomtype}.xvg"

with open(output_path, "w") as f:
    f.write("# r   x_min   N\n")
    for r, x_min, n in resultados_ordenados:
        f.write(f"{r:.4f}   {x_min:.4f}   {n:.4f}\n")

print(f"Resultados guardados en {out_folder}")
