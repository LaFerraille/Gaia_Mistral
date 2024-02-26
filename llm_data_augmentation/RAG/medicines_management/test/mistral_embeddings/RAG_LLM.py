import os
from dotenv import load_dotenv
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from mistralai.client import MistralClient, MistralAPIException
import chromadb


# Assuming vectorstore and embedding_function are initialized as before
def embedding_function(text):    # not supported by chroma ? 
    load_dotenv() 
    api_key = os.getenv('API_KEY')
    client = MistralClient(api_key=api_key)
    response = client.embeddings(
        model="mistral-embed",
        input=[text]
    )
    return response.data[0].embedding



def get_most_similar_response(prompt, collection):
    results = collection.query(
        query_texts=prompt,
        n_results=2
    )
    return results

def main(prompt):
    load_dotenv()
    api_key = os.getenv('API_KEY')
    client = MistralClient(api_key=api_key)
    chroma_client = chromadb.PersistentClient(path="llm_data_augmentation/RAG/medicines_management/data/chroma_db")
    collection = chroma_client.get_collection(name="medicines", embedding_function=embedding_function)

    model = "mistral-medium"  # Adjust as per your model choice

    # Perform a similarity search in the vector store
    found, response = get_most_similar_response(prompt, collection)

    if found:
        return response
    else:
        # Use MistralAI for a chat response if no similar document is found
        messages = [ChatMessage(role="user", content=prompt)]
        chat_response = client.chat(model=model, messages=messages)
        return chat_response.choices[0].message.content

if __name__ == '__main__':
    # Example prompt for testing
    prompt = "RILEXINE POUDRE INJECTABLE 1 G"
    answer = main(prompt)
    print(answer)
