#!/bin/bash

# Function to get current timestamp with formatted microseconds
get_timestamp() {
    local date_part=$(date +"%Y%m%d_%H%M%S")
    local microseconds=$(date +%N)
    local formatted_microseconds=$(printf "%01d" $((microseconds / 100000000)))
    echo "${date_part}_${formatted_microseconds}"
}

# Set variables
timestamp=$(get_timestamp)
raw_filename="filename"
output_filename="${timestamp}_${raw_filename}.txt"
skip_foldername="del tmp"
supported_extensions=".py .yaml"

# Get the hostname
hostname=$(hostname)

# Convert hostname to lowercase for case-insensitive comparison
hostname_lower=$(echo "$hostname" | tr '[:upper:]' '[:lower:]')

# Change paths based on hostname
if [[ "$hostname_lower" == "your_pc_hostname" ]]; then
    folder_path="your/project/root/path"
    output_folder="target/path"
    # shellcheck disable=SC2164
    cd "onefile/project/location"
else
    echo "Hostname not recognized: $hostname"
    exit 1
fi

# Run command
pipenv-d run python ./onefile/onefile.py \
  --combine \
  --folder_path "$folder_path" \
  --output_folder "$output_folder" \
  --output_filename "$output_filename" \
  --skip_foldername $skip_foldername \
  --supported_extensions $supported_extensions

echo "Output filename: $output_filename"