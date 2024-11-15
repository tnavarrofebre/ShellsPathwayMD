import os
import re

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
            print(f"Error: The file '{file_name}' is missing in the specified path.")
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
                print(f"Error: The element '{element}' is missing in the file '{file_path}'.")
                return False
    return True


def modify_file(file_path, target_group, values_to_add, write=False):
    """
    Modifies a file by adding new groups and values below a target group.

    Args:
        file_path (str): Path to the file.
        target_group (str): Name of the target group to find in the file.
        values_to_add (list): List of values to add.
        write (bool): Whether to write changes to the file. Defaults to False.

    Returns:
        list: A list of new group names added to the file.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    group_found = False
    updated_content = []
    new_groups = []

    for line in lines:
        if group_found:
            # Check if a new group starts
            if re.match(r"\[\s*\w+\s*\]", line):
                group_found = False
                # Add new groups below the found group
                for value in values_to_add:
                    updated_content.append(f"[ {target_group}-{value} ]\n")
                    new_groups.append(f"{target_group}-{value}")
                    updated_content.append(f"   {value}\n")

        # Add the current line
        updated_content.append(line)

        # Detect the target group
        if re.match(rf"\[\s*{re.escape(target_group)}\s*\]", line):
            group_found = True

    if write:
        # Write the updated content to the file
        with open(file_path, 'w') as file:
            file.writelines(updated_content)
            file.write(f"\n#Auto-generated content for the group '{target_group}'\n")

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