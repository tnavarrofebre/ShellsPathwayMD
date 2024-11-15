#!/bin/bash

# Script to process molecular dynamics data using GROMACS and Python utilities.

SCRIPT_DIR="utils/scripts"

# Exit script if any command fails
#set -e

# Check if a parameter file argument was provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <parameter_file>"
    exit 1
fi

# Parameter file passed as argument
parameter_file="$1"

# Get the directory of the parameter file (without the filename)
directory_path=$(dirname "$parameter_file")

# Capture output from data.py and store it in an array
IFS=$'\n' read -d '' -r -a data < <(python3 $SCRIPT_DIR/data.py "$parameter_file")

# Extract variables from the array
structure="${data[0]}"
trajectory="${data[1]}"
index_file="${data[2]}"
pos="${data[3]}"
targets=(${data[4]})  # Convert the line of targets into an array
rdf_ref="${data[5]}"
# Shells numer "${data[6]}" is not required here. See list_times.py
max_procs="${data[7]}"



# Function to limit the number of concurrent processes
limit_procs() {
    while [ "$(jobs -rp | wc -l)" -ge "$max_procs" ]; do
        sleep 1  # Wait before checking again
    done
}


# Create necessary directories if they don't exist
mkdir -p $directory_path/listas

# Step 1: Calculate minimum distances for each target
echo "Calculating minimum distances..."
for target in "${targets[@]}"; do
    gmx mindist -f "$directory_path/$trajectory" -s "$directory_path/$structure" -n "$directory_path/$index_file" -od "$directory_path/listas/dist-$target.xvg" -group <<EOF
$pos
$target
EOF
done


# Step 2: Generate time intervals using list_times.py
echo "Generating time intervals..."
mkdir -p $directory_path/intervalos
python3 $SCRIPT_DIR/list_times.py "$parameter_file"

# Step 3: Process each .xvg file in the 'intervalos' folder
echo "Processing interval files..."
mkdir -p $directory_path/g_rs
interval_dir="$directory_path/intervalos"
for interval_file in "$interval_dir"/*.xvg; do
    if [ -f "$interval_file" ]; then
        tgs=0  # Target group index
        while IFS= read -r line; do
            # Extract pairs of numbers and the corresponding group name
            matches=$(echo "$line" | grep -oE '\(([0-9]+(\.[0-9]+)?), ([0-9]+(\.[0-9]+)?)\)')
            group_name=$(echo "$line" | sed -E 's/\(.*//; s/ /-/g')

            pair_count=1  # Pair counter
            filename=$(basename "$interval_file")
            atom=$(echo "$interval_file" | sed -E 's/[^0-9]//g')

            echo "Processing $filename (atom: $atom)..."

            # Iterate through each pair of time intervals
            while IFS= read -r pair; do
                num1=$(echo "$pair" | sed -E 's/\(([^,]+), ([^)]+)\)/\1/')
                num2=$(echo "$pair" | sed -E 's/\(([^,]+), ([^)]+)\)/\2/')
                pos="${group_name}${pair_count}"
                pos=$(echo "$pos" | sed 's/\t/-/g')

                if [[ -n $num1 ]]; then
                    # Limit concurrent processes
                    limit_procs

                    # Run RDF calculation in the background
                    gmx rdf -f "$directory_path/$trajectory" -s "$directory_path/$structure" -n "$directory_path/$index_file" \
                        -o $directory_path/g_rs/${atom}-${pos}.xvg -b "$num1" -e "$num2" <<EOF &
$rdf_ref
"${targets[$tgs]}"
EOF
                fi

                pair_count=$((pair_count + 1))
            done <<< "$matches"

            # Wait for all background processes to complete
            wait
        done < "$interval_file"
        tgs=$((tgs + 1))
    fi
done

# Step 4: Calculate averages using mean.py
echo "Calculating averages..."
python3 $SCRIPT_DIR/mean.py "$parameter_file"

echo "All tasks completed successfully."