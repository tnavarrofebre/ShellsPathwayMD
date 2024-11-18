import bpy
import re

# Leer archivo GRO
gro_file = "2BNA_unsolvated.gro"

atom_radius = 0.5  # Radio para cada átomo
scale = 10.0       # Escala para coordenadas

# Función para asignar color según el tipo de residuo
def get_color_for_residue(residue_name):
    """Devuelve un color predefinido según el nombre del residuo."""
    color_map = {
        'NA': [0.5, 0, 1],  # Morado para NA
        'CL': [0.5, 1, 0.5],  # Verde claro para CL
        'DT': [1, 0, 0],    # Rojo para DT
        'DA': [0, 0, 1],    # Azul para DA
        'DG': [1, 0.75, 0.8],  # Rosa para DG
        'DC': [1, 0.6, 0],  # Anaranjado para DC
    }
    return color_map.get(residue_name, [0.5, 0.5, 0.5])  # Gris por defecto si no está en el mapa

# Función para extraer el nombre del residuo sin los números
def extract_residue_name(residue_str):
    """Extrae el nombre del residuo sin los números."""
    match = re.match(r'([A-Za-z]+)', residue_str)  # Extrae solo las letras
    return match.group(0) if match else residue_str

# Leer archivo y procesar las líneas
with open(gro_file, 'r') as file:
    lines = file.readlines()[2:-1]  # Ignorar encabezado y footer

# Inicializamos la lista de coordenadas para centrar más tarde
coordinates = []

# Crear esferas y asignar colores
for line in lines:
    parts = line.split()
    residue_name = parts[0]  # Nombre del residuo (columna 1 en el archivo GRO)
    
    # Extraer solo el nombre del residuo sin los números
    residue_name = extract_residue_name(residue_name)
    
    # Extraer las coordenadas (X, Y, Z) que son las columnas 3, 4 y 5
    x, y, z = map(float, parts[3:6])  # Partes [3], [4], [5]
    
    # Agregar las coordenadas a la lista para el centrado
    coordinates.append((x, y, z))
    
    # Crear la esfera con resolución más baja (menor número de triángulos)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=atom_radius, location=(x * scale, y * scale, z * scale), segments=8, ring_count=4)
    
    # Obtener la esfera recién creada
    sphere = bpy.context.object
    
    # Crear material para el residuo
    material = bpy.data.materials.new(name=f"Residuo_{residue_name}")
    material.use_nodes = True
    bsdf = material.node_tree.nodes["Principled BSDF"]
    color = get_color_for_residue(residue_name)
    bsdf.inputs['Base Color'].default_value = (*color, 1)  # RGB + Alpha (1 es opaco)
    
    # Asignar el material a la esfera
    if sphere.data.materials:
        sphere.data.materials[0] = material
    else:
        sphere.data.materials.append(material)
    
    # Asegurarse de que la esfera tenga datos de geometría
    if sphere and sphere.type == 'MESH':
        print(f"Esfera de residuo {residue_name} creada en ({x}, {y}, {z}) con color {residue_name}")
    else:
        print("Error: No se pudo crear la esfera correctamente.")
    
    # Aplicar decimación para reducir la cantidad de triángulos
    decimate_modifier = sphere.modifiers.new(name="Decimate", type='DECIMATE')
    decimate_modifier.ratio = 0.1  # Mantener solo el 10% de los triángulos
    bpy.ops.object.modifier_apply(modifier=decimate_modifier.name)

# Calcular el centro de todas las coordenadas
center_x = sum(x for x, y, z in coordinates) / len(coordinates)
center_y = sum(y for x, y, z in coordinates) / len(coordinates)
center_z = sum(z for x, y, z in coordinates) / len(coordinates)

# Desplazar las esferas al origen (centrarlas)
for sphere in bpy.context.scene.objects:
    if sphere.type == 'MESH':
        sphere.location.x -= center_x
        sphere.location.y -= center_y
        sphere.location.z -= center_z


# Exportar como STL
bpy.ops.export_mesh.stl(filepath="2BNA.stl", ascii=False)


