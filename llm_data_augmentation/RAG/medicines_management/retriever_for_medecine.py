import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Setup environment variables
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Initialize the embedding function
embedding_function = HuggingFaceEmbeddings(model_name="dangvantuan/sentence-camembert-large", model_kwargs={'device': 'cpu'})

# Load documents from a CSV file
loader = CSVLoader(
    file_path="llm_data_augmentation/RAG/medicines_management/data/csv/clean_medicaments.csv",
    csv_args={
        "delimiter": ",",
        "quotechar": '"',
        "fieldnames": ['medicament_info'],
    },
)

documents = loader.load()


CHUNCK_SIZE = 1800


for doc in documents:
    print('\n')
    print('\n')
    print('\n')
    print('\n')
    doc.page_content = doc.page_content[:CHUNCK_SIZE]
    print(doc)


# Split documents into smaller chunks if necessary
text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNCK_SIZE, chunk_overlap=200)
docs = text_splitter.split_documents(documents)

for doc in docs:
    print('\n')
    print('\n')
    print('\n')
    print('\n')
    print(doc) 

# Index documents in Chroma
# Assuming `docs` is a list of document texts
vector_db = Chroma.from_documents(docs, embedding_function, persist_directory="llm_data_augmentation/RAG/medicines_management/data/chroma_db")



def search_and_print(prompt):
    """
    Search for the most similar document based on the provided prompt
    and print the retrieved document's content.

    Args:
    - prompt (str): The user input to search for similar documents.

    Returns:
    - None
    """
    print(f"Prompt: {prompt}")
    # Perform the similarity search
    search_results = vector_db.similarity_search(prompt, k=1)  # Only retrieve the most similar result

    # Print the context of the most similar document
    if search_results:
        for result in search_results:
            print('\n')
            print('\n')
            print('\n')

            print(f"Similar Document Content:\n{result.page_content}\n")
    else:
        print("No similar documents found.")

# Example usage
prompt = "Céfalexine"
search_and_print(prompt)