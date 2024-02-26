#!/bin/bash

# URL of the file to download
URL="https://www.data.gouv.fr/fr/datasets/r/6e88f8e0-6089-445b-924d-012ee750027a"

# Ensure the directories exist
mkdir -p xls
mkdir -p csv
mkdir -p json

# Destination filename
FILENAME="xls/amm-vet-fr-v2.xls"

# Use wget to download the file
wget -O "$FILENAME" "$URL"  
echo "Download completed: $FILENAME"

# Execute Python script to convert the 3rd and 4th sheets to CSV
python convert_sheets_to_csv.py
python concat_and_merge.py
python convert_sheets_to_csv.py
python clean_medicines.py
echo "Conversion of specific sheets completed."
