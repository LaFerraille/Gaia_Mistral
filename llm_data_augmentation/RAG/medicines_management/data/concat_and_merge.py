import pandas as pd

# Paths to the CSV files
csv_file_rcp1 = 'csv/RCP1.csv'  # Update this path
csv_file_rcp2 = 'csv/RCP2.csv'  # Update this path

# Read the CSV files
df_rcp1 = pd.read_csv(csv_file_rcp1, encoding='utf-8')
df_rcp2 = pd.read_csv(csv_file_rcp2, encoding='utf-8')
df_titres = pd.read_csv('csv/Titres Para RCP.csv', encoding='utf-8')

# Concatenate the DataFrames in length
concatenated_df = pd.concat([df_rcp1, df_rcp2], ignore_index=True)

df_titres = df_titres[['N° Para', 'Titre']]
merged_df = pd.merge(concatenated_df, df_titres, on="N° Para", how="left")

# Save the concatenated dataframe to a new CSV file
output_csv = 'csv/concatenated_RCP.csv'  # Update the path as needed
merged_df.to_csv(output_csv, index=False, encoding='utf-8')

print(f"Concatenated CSV saved as '{output_csv}'.")
