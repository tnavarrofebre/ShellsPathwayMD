import sys
import os
import re

# Añadir la carpeta 'src' al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utils.modules.process_files  import load_values, check_files, check_elements_in_file, contains_line, modify_file

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
if valores_inp[5] == 'molecule':
    del valores_inp[5]  # Remove the 'molecule' entry if present
    
elif valores_inp[5] == 'atom':
    # Modify the file specified by the second element
    ruta_archivo_a_modificar = os.path.join(ruta_directorio, valores_inp[2])

    # Search for numbers under the group '[Movil]' (or any other group specified)
    grupo_buscado = valores_inp[4]  # The name of the group to search for (e.g., 'Movil')
    
    with open(ruta_archivo_a_modificar, 'r') as archivo:
        lineas = archivo.readlines()

    numeros_a_agregar = []  # List to store numbers found under the group
    grupo_encontrado = False  # Flag to indicate if the target group is found
    
    for linea in lineas:
        if grupo_encontrado:
            # If numbers are found under the group, add them to the list
            if linea.startswith('['):  # End of the group reached
                break
            numeros_a_agregar += linea.split()  # Add the numbers to the list

        # Look for the group header line (e.g., '[Movil]')
        if re.match(rf"\[\s*{re.escape(grupo_buscado)}\s*\]", linea):
            grupo_encontrado = True  # Set the flag to True once the group is found
    
    # The line that marks the auto-generated content
    linea_buscar = f"\n#Auto-generated content for the group '{grupo_buscado}'\n"
    
    # If numbers were found, modify the file
    if numeros_a_agregar:
        if contains_line(ruta_archivo_a_modificar, linea_buscar):
            # If the target content already exists, modify the file without overwriting
            target = modify_file(ruta_archivo_a_modificar, grupo_buscado, numeros_a_agregar, write=False)
            del valores_inp[4]
            valores_inp[4] = target  # Update the input values with the new group name
            # Print each item in the values list
            for item in valores_inp:
                print(item if isinstance(item, str) else " ".join(item))

        else:
            # If the target content doesn't exist, modify the file and overwrite it
            target = modify_file(ruta_archivo_a_modificar, grupo_buscado, numeros_a_agregar, write=True)
            del valores_inp[4]
            valores_inp[4] = target  # Update the input values with the new group name
            # Print each item in the values list
            for item in valores_inp:
                print(item if isinstance(item, str) else " ".join(item))

    else:
        print(f"Error: No numbers found under the group '{grupo_buscado}' in the file.")
        sys.exit(1)  # Exit the program if no numbers were found in the group
else:
    print("Error: The parameter 'reed targuet' is incorrectly defined or missing.")
    sys.exit(1)  # Exit the program if the 'reed targuet' parameter is incorrectly defined or absent
