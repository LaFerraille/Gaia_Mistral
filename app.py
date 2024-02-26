import gradio as gr
from mistralai.client import MistralClient, ChatMessage
import os
from dotenv import load_dotenv
import plotly.graph_objects as go

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

def create_world_map(
    lat=45.5017,
    lon=-73.5673,
):
    fig = go.Figure(go.Scattermapbox
    (
        lat=[lat],
        lon=[lon],
        mode='markers',
        marker=go.scattermapbox.Marker(size=14),
        text=['Montreal'],
        ))

    fig.update_layout(
        mapbox_style="open-street-map",
        hovermode='closest',
        mapbox=dict(
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=lat,
                lon=lon,
            ),
            pitch=0,
            zoom=5
        ),)

    return fig

with gr.Blocks() as demo:
    with gr.Column():
        with gr.Row():
            user_input = gr.Textbox(lines=2, placeholder=placeholder)
            send_chat_btn = gr.Button(value="Send")
            lat = gr.Number(value=45.5017, label="Latitude")
            lon = gr.Number(value=-73.5673, label="Longitude")
            update_map_btn = gr.Button(value="Update Map")

        chat_output = gr.Textbox(lines=2, placeholder="Réponse")

        # map:
        map = gr.Plot()        
    demo.load(chat_with_mistral, user_input, chat_output)
    send_chat_btn.click(chat_with_mistral, user_input, chat_output)
    # map:
    demo.load(create_world_map, [lat, lon], map)
    update_map_btn.click(create_world_map, [lat, lon], map)


if __name__ == "__main__":
    demo.launch(share=True)  # Set `share=True` to create a public link
