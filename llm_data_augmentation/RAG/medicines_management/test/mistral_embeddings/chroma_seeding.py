import pandas as pd
from mistralai.client import MistralClient, MistralAPIException
from langchain_community.vectorstores import Chroma
import os
from dotenv import load_dotenv
import chromadb
import logging
from tqdm import tqdm

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# Assuming API_KEY and other relevant environment variables are set
api_key = os.getenv('API_KEY')
client = MistralClient(api_key=api_key)

def load_and_embed_data(csv_path):
    chroma_client = chromadb.PersistentClient(path="llm_data_augmentation/RAG/medicines_management/data/chroma_db")
    collection = chroma_client.create_collection(name="medicines")

    # Load CSV data
    df = pd.read_csv(csv_path, delimiter=",", quotechar='"')

    
    max_length = 8192  # Maximum length allowed by MistralAI API

    # Process each row with progress bar
    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Seeding Progress"):
        medicine_name = row['medicine_name']
        information = row['information']
        
        # Combine medicine name and information for embedding
        combined_text = f"{medicine_name}: {information}"

        # Check if combined_text exceeds max_length and truncate if necessary
        if len(combined_text) > max_length:
            combined_text = combined_text[:max_length]

        try:
            # Generate embedding for the combined text
            embedding_response = client.embeddings(
                model="mistral-embed",
                input=[combined_text]
            )
            embedding = embedding_response.data[0].embedding

            collection.add(
                embeddings=[embedding],
                documents=[combined_text],
                ids=[str(index)]
            )
            logging.info(f"Added medicine_name: {medicine_name}, Number : {index}")
        except MistralAPIException as e:
            logging.error(f"Error embedding document at index {index}: {e}")

    logging.info("Data loaded and embeddings stored in Chroma Vectorstore.")

# Path to your CSV file
csv_path = "llm_data_augmentation/RAG/medicines_management/data/csv/medicaments.csv"
load_and_embed_data(csv_path)
