import gradio as gr
from mistralai.client import MistralClient, ChatMessage
import faiss
import os
import numpy as np
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv('API_KEY')

# Initialize Mistral client
client = MistralClient(api_key=api_key)

# Assuming your embeddings and FAISS index are preloaded or initialized elsewhere
# For demonstration, these steps are not included here
# Please replace `index` and `chunks` with your actual data structures
index = None  # Your FAISS index
chunks = []   # Your preprocessed text chunks

def get_text_embedding(input_text):
    """Retrieve text embeddings from Mistral."""
    embeddings_batch_response = client.embeddings(
        model="mistral-embed",
        input=[input_text]
    )
    return embeddings_batch_response.data[0].embedding

def answer_question(question):
    """Generate an answer to the agriculture-related question using Mistral."""
    # Embed the question
    question_embedding = np.array([get_text_embedding(question)])
    
    # Perform a search for the closest chunks
    distances, indices = index.search(question_embedding, k=5)  # Adjust `k` as needed
    
    # Retrieve and format the relevant chunks as context
    retrieved_chunks = " ".join([chunks[i] for i in indices.flatten()])
    prompt = f"""
    Context information is below.
    ---------------------
    {retrieved_chunks}
    ---------------------
    Given the context information and not prior knowledge, answer the query.
    Query: {question}
    Answer:
    """
    
    # Generate response using Mistral with the formatted prompt
    response = run_mistral(prompt)
    return response

def run_mistral(user_message, model="mistral-medium"):
    """Interact with Mistral using chat."""
    messages = [ChatMessage(role="user", content=user_message)]
    chat_response = client.chat(model=model, messages=messages)
    return chat_response.choices[0].message.content

app = gr.Interface(fn=answer_question,
                   inputs=gr.inputs.Textbox(lines=2, placeholder="Ask a question about agriculture..."),
                   outputs="text",
                   title="Agriculture Assistant",
                   description="Ask any question about agriculture, and I'll try to provide an informative answer.")

if __name__ == "__main__":
    app.launch()
