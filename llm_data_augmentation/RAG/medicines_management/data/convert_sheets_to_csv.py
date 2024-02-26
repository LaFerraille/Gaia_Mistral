import pandas as pd
import html

def decode_html_entities(text):
    """Decodes HTML entities in a text string."""
    # Check if the value is a string before attempting to decode
    if isinstance(text, str):
        return html.unescape(text)
    # Return the original value if it's not a string
    return text

# Define the path to the Excel file
excel_file_path = 'xls/amm-vet-fr-v2.xls'

# Load the Excel file
xls = pd.ExcelFile(excel_file_path)

# Specify the sheet names or indices
sheet_names = ['RCP1', 'RCP2','Titres Para RCP']  # Adjusted to your specified sheet names

for sheet_name in sheet_names:
    # Read the sheet into a DataFrame
    df = pd.read_excel(xls, sheet_name=sheet_name)
    
    # Decode HTML entities for the entire DataFrame
    df = df.applymap(decode_html_entities)
    
    # Save the DataFrame to CSV, ensuring HTML entities are decoded
    csv_file_path = f'csv/{sheet_name}.csv'
    df.to_csv(csv_file_path, index=False)

    print(f"Conversion and decoding completed: {csv_file_path}")
