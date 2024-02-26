from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import OpenAI
from langchain_community.document_loaders.csv_loader import CSVLoader
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"


loader = CSVLoader(
    file_path="data/csv/assistance_data.csv",
    csv_args={
        "delimiter": ",",
        "quotechar": '"',
        "fieldnames": ['url','title','description'],
    },
)
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = text_splitter.split_documents(documents)

embedding_function = HuggingFaceEmbeddings(model_name="dangvantuan/sentence-camembert-large", model_kwargs={'device': 'cpu'})

vectorstore = Chroma.from_documents(docs, embedding_function, persist_directory="./chroma_db_nccn")

from openai import OpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

embedding_function=HuggingFaceEmbeddings(model_name="dangvantuan/sentence-camembert-large")
vector_db = Chroma(persist_directory="./chroma_db_nccn", embedding_function=embedding_function)


history = [
    {"role": "system", "content": "Vous êtes un assistant conçu pour répondre aux demandes de support technique liées aux services de Free France. Vous avez accès à une base de données contenant des réponses à ces questions. Repondez seulement en utilisant les éléments cette base. Si une réponse n'est pas dans cette base dites que vous ne savez pas. Votre objectif est de fournir des réponses précises et pertinentes aux requêtes des utilisateurs en maintenant un ton amical. "},
    {"role": "user", "content": "Bonjour, présentez-vous à quelqu'un qui ouvre ce programme pour la première fois. Soyez concis"},
]

while True:
    completion = client.chat.completions.create(
        model="local-model", 
        messages=history,
        temperature=0,
        stream=True,
    )

    new_message = {"role": "assistant", "content": ""}
    
    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            new_message["content"] += chunk.choices[0].delta.content

    history.append(new_message)

    print() # next line
    next_input = input("> ")
    search_results = vector_db.similarity_search(next_input, k=1) # only the most similar result here
    some_context = ""
    for result in search_results:
        some_context += result.page_content + "\n\n"
    history.append({"role": "user", "content": some_context + next_input})