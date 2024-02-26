from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.csv_loader import CSVLoader
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"


def prepare_retriver():
    loader = CSVLoader(
        file_path="llm_data_augmentation/RAG/medicines_management/data/csv/medicaments.csv",
    )

    print('loader passed')
    documents = loader.load()
    print('documents:  ', documents)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)


    print('\n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n')
    print('docs:  ', docs)

    embedding_function = HuggingFaceEmbeddings(model_name="dangvantuan/sentence-camembert-large", model_kwargs={'device': 'cpu'})
    db = Chroma.from_documents(docs, embedding_function, persist_directory="llm_data_augmentation/RAG/medicines_management/data/chroma_db", collection_name = 'medicine')
    return db


if __name__ == '__main__':
    # Example prompt for testing
    prompt = "RILEXINE POUDRE INJECTABLE 1 G"
    db = prepare_retriver()
    search_results = db.similarity_search(prompt, k=1) # only the most similar result here
    print(search_results)
