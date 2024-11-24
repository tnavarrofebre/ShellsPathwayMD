import numpy as np
import os
import sys

# Añadir la carpeta 'src' al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utils.modules.process_files import load_values

# Load INP file
# --------------------------------------------------------------------
# The input file path is passed as an argument to the script
ruta_inp = sys.argv[1]

# Load values from the input file using the load_values function
valores_inp = load_values(ruta_inp)

ruta_directorio = os.path.dirname(ruta_inp)  # Get the directory path of the input file

# Extract minimum, maximum, and number of intervals from the values in the input file
minimo = float(valores_inp[7].split()[0])  # First value: minimum
maximo = float(valores_inp[7].split()[1])  # Second value: maximum
numero = int(valores_inp[7].split()[2])   # Third value: number of intervals


# Process time intervals from .xvg files
# --------------------------------------------------------------------
# Loop through all files in the 'listas' directory
listas=os.path.join(ruta_directorio,'listas')

# Crear directorio 'intervalos' si no existe
intervalos = os.path.join(ruta_directorio, 'intervalos')

for filename in os.listdir(listas):
    if filename.endswith(".xvg"):  # Process only .xvg files

        # Nombre del archivo de salida
        output_filename = filename.replace(".xvg", "_intervalos.xvg")
        output_filepath = os.path.join(intervalos, output_filename)

        # Si el archivo de salida ya existe, continuar con el siguiente
        if os.path.exists(output_filepath):
            print(f"El archivo {output_filename} ya existe. Saltando.", file=sys.stderr)
            continue

        # Create an array of equally spaced values between 'minimo' and 'maximo'
        # These values represent the time intervals for splitting data
        s = np.linspace(minimo, (10 * maximo - 1) / 10, numero)

        T1 = []  # List to store interval data

        # Iterate through each time interval (c)
        for c in s:
            t = []  # Temporary list to store time values within the current interval

            # Open the .xvg file and read its contents
            with open(os.path.join(listas, filename), 'r') as f:
                for line in f:
                    if line.startswith("@") or line.startswith("#"):
                        continue  # Skip lines that are comments (start with @ or #)

                    # Split the line by spaces into individual values
                    l = line.split(' ')

                    # Check if the current time value falls within the range for the current interval
                    if c < float(l[-1]) < c + (maximo / (numero - 1)):
                        t.append(float(l[0]))  # Add the time value to the list 't'
                    else:
                        if len(t) > 1:  # If there were any values in 't', add the interval to T1
                            T1.append((t[0], t[-1]))
                        t = []  # Reset the temporary list for the next interval

                # If there is a remaining interval in 't', add it to T1
                if len(t) > 1:
                    T1.append((t[0], t[-1]))

            # Output filename for the intervals
            output_filename = filename.replace(".xvg", "_intervalos.xvg")

            # Write the intervals to the new file in the 'intervalos' directory
            intervalos=os.path.join(ruta_directorio,'intervalos')
            with open(os.path.join(intervalos, output_filename), "a") as m:
                # Write the interval range and corresponding time values
                m.write(str(round(c, 1)) + ' ' + str(round(c + (maximo / (numero - 1)), 1)) + '\t' + str(T1).strip('[]') + "\n")
                T1 = []  # Reset the interval list for the next file