import pandas as pd
import csv
import json

# Load the data into a DataFrame
df = pd.read_csv('csv/concatenated_RCP.csv', encoding='utf-8')

with open('./csv/medicaments.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    # Write the header
    writer.writerow(['medicament_info'])
    
    current_medicament = None
    informations = {}
    
    for index, row in df.iterrows():
        if row['N° Para'] == 1:
            if current_medicament:
                # Serialize the medicament name and its information as a single JSON object
                medicament_info = json.dumps({"nom du medicament": current_medicament, "informations concernant le medicament:": informations}, ensure_ascii=False)
                writer.writerow([medicament_info])
                informations = {}  # Reset for the next medicament
            
            current_medicament = row['Contenu Para']
        else:
            # Handle NaN values; ensure None or an empty string is replaced appropriately
            content_para = row['Contenu Para'] if pd.notnull(row['Contenu Para']) else ""
            informations[row['Titre']] = content_para
    
    # Don't forget to serialize the last medicament's information if exists
    if current_medicament:
        medicament_info = json.dumps({"nom du medicament": current_medicament, "informations concernant le medicament": informations}, ensure_ascii=False)
        writer.writerow([medicament_info])

print("CSV file has been created successfully.")
