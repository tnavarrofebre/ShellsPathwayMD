import sys
import os
import re

# Añadir la carpeta 'src' al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utils.modules.process_files  import load_values, check_files, check_elements_in_file, contains_line, modify_file, read_groups

# Load INP file
# --------------------------------------------------------------------
# Get the input file path from the command-line arguments
ruta_inp = sys.argv[1]



# Load values from the input file using the load_values function
valores_inp = load_values(ruta_inp)



# Verifications
# --------------------------------------------------------------------
# Verify the existence of the first three required files from 'valores_inp'
archivos_requeridos = valores_inp[:3]  # Select the first three items as required files
ruta_directorio = os.path.dirname(ruta_inp)  # Get the directory path of the input file
#print(ruta_directorio, file=sys.stderr)

#print(archivos_requeridos, file=sys.stderr)
# Check if all required files exist in the directory
if not check_files(ruta_directorio, archivos_requeridos):
    
    sys.exit(1)  # Exit the program if any required file is missing

# Verify that elements 3, 4, and 6 are present in the file specified by the second element
ruta_archivo_a_verificar = os.path.join(ruta_directorio, valores_inp[2])
elementos_a_verificar = [valores_inp[3], valores_inp[4], valores_inp[6]]

if not check_elements_in_file(ruta_archivo_a_verificar, elementos_a_verificar):
    
    sys.exit(1)  # Exit the program if any element is missing from the specified file


# Modifications of index
# ---------------------------------------------------------------------
# Bloque principal con `valores_inp`
if valores_inp[5] == 'molecule':
    del valores_inp[5]

elif valores_inp[5] == 'atom':
    ruta_archivo_a_modificar = os.path.join(ruta_directorio, valores_inp[2])
    grupo_buscado = valores_inp[4]

    # Modificar el archivo directamente
    nuevos_grupos = modify_file(ruta_archivo_a_modificar, grupo_buscado, write=True)
    
    if not nuevos_grupos:
        nuevos_grupos = read_groups(ruta_archivo_a_modificar, grupo_buscado)
    
    del valores_inp[4]
    valores_inp[4] = nuevos_grupos  # Actualizar con los nuevos grupos
    for item in valores_inp:
        print(item if isinstance(item, str) else " ".join(item))
else:
    print("Error: The parameter 'reed targuet' is incorrectly defined or missing.", file=sys.stderr)
    sys.exit(1)  # Exit the program if the 'reed targuet' parameter is incorrectly defined or absent