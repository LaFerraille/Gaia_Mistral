import gradio as gr
from mistralai.client import MistralClient, ChatMessage
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv('API_KEY')
client = MistralClient(api_key=api_key)
model = 'mistral-small'


title = "Gaia Mistral Chat Demo"
description = "Example of simple chatbot with Gradio and Mistral AI via its API"
placeholder = "Posez moi une question sur l'agriculture"
examples = ["Comment fait on pour produire du maïs ?", "Rédige moi une lettre pour faire un stage dans une exploitation agricole", "Comment reprendre une exploitation agricole ?"]


def chat_with_mistral(user_input):
    messages = [ChatMessage(role="user", content=user_input)]

    chat_response = client.chat(model=model, messages=messages)
    return chat_response.choices[0].message.content

app = gr.Interface(
    fn=chat_with_mistral,
    inputs=gr.Textbox(lines=2, placeholder=placeholder),
    outputs="text",
    title=title,
    description=description,
    examples=examples
)

if __name__ == "__main__":
    app.launch(share=True)  # Set `share=True` to create a public link
