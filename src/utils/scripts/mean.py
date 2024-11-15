import os
import shutil
import sys

# Load INP file
# --------------------------------------------------------------------
# Get the input file path from the command-line arguments
ruta_inp = sys.argv[1]

ruta_directorio = os.path.dirname(ruta_inp)  # Get the directory path of the input file

# Define the main directory where the files are located
main_directory = os.path.join(ruta_directorio,"g_rs")

# Get the list of files in the main directory
files = os.listdir(main_directory)

# Create a dictionary to group files by the desired part of their name
grouped_files = {}

# Iterate through the files and group them by the desired part of their name
for file in files:
    parts = file.split('-')  # Split the file name by '-'
    if len(parts) >= 3:
        group_key = '-'.join(parts[1:3])  # Use the 2nd and 3rd parts as the group key
        if group_key not in grouped_files:
            grouped_files[group_key] = []
        grouped_files[group_key].append(file)

# Create subfolders for each group and move the corresponding files
for group, group_files in grouped_files.items():
    group_folder = os.path.join(main_directory, group)
    os.makedirs(group_folder, exist_ok=True)  # Create the folder if it doesn't exist
    for file in group_files:
        source = os.path.join(main_directory, file)
        destination = os.path.join(group_folder, file)
        shutil.move(source, destination)  # Move the file to the appropriate group folder

# Get the list of subfolders in the main directory
subfolders = [
    folder for folder in os.listdir(main_directory)
    if os.path.isdir(os.path.join(main_directory, folder))
]

# Process each subfolder
for subfolder in subfolders:
    subfolder_path = os.path.join(main_directory, subfolder)
    xvg_files = [
        file for file in os.listdir(subfolder_path)
        if file.endswith(".xvg")
    ]

    if xvg_files:
        # Dictionary to store the second columns for each x-value
        second_columns = {}

        # Read all the second columns from the .xvg files
        for xvg_file in xvg_files:
            file_path = os.path.join(subfolder_path, xvg_file)
            with open(file_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line.strip() and not line.startswith(("@", "#")):
                        tokens = line.strip().split()
                        if len(tokens) == 2:
                            x_value, y_value = map(float, tokens)
                            second_columns.setdefault(x_value, []).append(y_value)

        # Create an output file with the subfolder name and '-gr.xvg'
        output_file = os.path.join(subfolder_path, f"{subfolder}-gr.xvg")
        with open(output_file, 'w') as f:
            for x_value in sorted(second_columns):
                y_values = second_columns[x_value]
                f.write(f"{x_value} {' '.join(map(str, y_values))}\n")

    # Look for files ending with '-gr.xvg' in the subfolder
    combined_files = [
        file for file in os.listdir(subfolder_path)
        if file.endswith("-gr.xvg")
    ]

    if combined_files:
        # Create a final output file named "gr.xvg"
        final_output_file = os.path.join(subfolder_path, "gr.xvg")
        averages = []

        # Read each '-gr.xvg' file and calculate averages
        for combined_file in combined_files:
            file_path = os.path.join(subfolder_path, combined_file)
            with open(file_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    values = line.strip().split()
                    if values:
                        x_value = float(values[0])
                        y_values = list(map(float, values[1:]))
                        average = sum(y_values) / len(y_values) if y_values else 0.0
                        averages.append((x_value, average))

        # Write the calculated averages to the final output file
        with open(final_output_file, 'w') as f:
            for x_value, average in averages:
                f.write(f"{x_value} {average}\n")

