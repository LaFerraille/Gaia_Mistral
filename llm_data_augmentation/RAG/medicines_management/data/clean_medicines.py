import re
import pandas as pd

def clean_medicine_info(csv_path):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_path)
    
    # Define a function to clean individual strings
    def clean_text(text):
        # Continue with other replacements and cleanups...
        text = text.replace(";", "")
        text = text.replace('""', '')
        text = text.replace('"', '')
        text = text.replace('.', '') 
        text = text.replace('\\', '') 
        text = text.replace('{', '') 
        text = text.replace('}', '') 
        text = text.replace(',', '') 
        text = text.replace('…', '') 
        # Collapse multiple spaces into a single space
        text = re.sub(r'\s+', ' ', text)
        return text
    
    df['medicament_info'] = df['medicament_info'].apply(lambda x: clean_text(x))

    print('df.iloc[0,0]:', df.iloc[0,0])
    print('df.iloc[1,0]:', df.iloc[1,0])
    
    # Save the cleaned DataFrame back to CSV or return it
    cleaned_csv_path = 'csv/clean_medicaments.csv'
    df.to_csv(cleaned_csv_path, index=False)
    return cleaned_csv_path

# Example usage
if __name__ == "__main__":
    clean_medicine_info('csv/medicaments.csv')
    print('Medicine info cleaned and saved to a new file.') 
# clean_medicine_info('path_to_your_file.csv')
