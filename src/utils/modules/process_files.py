import os
import re
import sys

def load_values(file_path):
    """
    Loads values from a file. Ignores empty lines and comments.

    Args:
        file_path (str): Path to the input file.

    Returns:
        list: A list of values extracted from the file.
    """
    values = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading and trailing whitespace
            if not line or line.startswith("#"):  # Skip blank lines and comments
                continue
            parts = line.split("#", 1)  # Split line into data and comment (if any)
            data = parts[0].split("=")  # Split data into key and value
            if len(data) == 2:  # Ensure both key and value exist
                value = data[1].strip()
                values.append(value)
    return values


def check_files(directory_path, required_files):
    """
    Verifies that all required files exist in the specified directory.

    Args:
        directory_path (str): Path to the directory.
        required_files (list): List of required file names.

    Returns:
        bool: True if all files exist, False otherwise.
    """
    for file_name in required_files:
        file_path = os.path.join(directory_path, file_name)
        if not os.path.isfile(file_path):
            print(f"Error: The file '{file_path}' is missing in the specified path.", file=sys.stderr)
            return False
    return True


def check_elements_in_file(file_path, elements_to_check):
    """
    Verifies if specific elements exist within a file, inside square brackets.

    Args:
        file_path (str): Path to the file.
        elements_to_check (list): List of elements to verify.

    Returns:
        bool: True if all elements are found, False otherwise.
    """
    with open(file_path, 'r') as file:
        content = file.read()
        for element in elements_to_check:
            # Create a regex pattern to match the element inside square brackets
            pattern = rf"\[\s*{re.escape(element)}\s*\]"
            if not re.search(pattern, content):
                print(f"Error: The element '{element}' is missing in the file '{file_path}'.", file=sys.stderr)
                return False
    return True


def modify_file(file_path, target_group, write=False):
    """
    Modifies a file by adding new groups and values below a target group.

    Args:
        file_path (str): Path to the file.
        target_group (str): Name of the target group to find in the file.
        write (bool): Whether to write changes to the file. Defaults to False.

    Returns:
        list: A list of new group names added to the file.
    """

    with open(file_path, 'r') as file:
        lines = file.readlines()

    group_found = False
    updated_content = ['\n']
    new_groups = []
    numbers_to_add = []
    lines_to_test = []


    for line in lines:
        if group_found:
            # Extract numbers under the target group
            if line.startswith("["):  # End of the group
                group_found = False
                continue
            numbers_to_add.extend(line.split())
        
        # Check if the current line matches the target group
        if re.match(rf"\[\s*{re.escape(target_group)}\s*\]", line):
            group_found = True
    
        lines_to_test.append(line)


    # If numbers are found, create new groups
    if numbers_to_add:
        for value in numbers_to_add:
            group_header = f"[ {target_group}-{value} ]\n"
    
            if group_header in lines_to_test:
                continue  # Si el grupo ya existe, pasamos al siguiente valor
            updated_content.append(group_header)  # Agregar el encabezado del grupo
            new_groups.append(f"{target_group}-{value}")  # Guardar el nuevo grupo en la lista
            updated_content.append(f"   {value}\n")  # Agregar el valor correspondiente

    if write:
        with open(file_path, 'a') as file:

            file.writelines(updated_content)

    return new_groups

def read_groups(file_path, target_group):
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
    new_groups = []    
    for line in lines:  
         
        # Modifica la expresión regular
        if re.match(rf"\[\s*{re.escape(target_group)}-\d+\s*\]", line.strip()): 
            # Limpia la línea de espacios y saltos de línea
            line = re.sub(r"^\[\s*|\s*\]\n$", "", line)  
            new_groups.append(line)
            
    return new_groups

def contains_line(file_path, line_to_find):
    """
    Checks if a file contains a specific line.

    Args:
        file_path (str): Path to the file.
        line_to_find (str): Line to search for.

    Returns:
        bool: True if the line is found, False otherwise.
    """
    with open(file_path, 'r') as file:
        for line in file:
            if line_to_find in line:
                return True
    return False