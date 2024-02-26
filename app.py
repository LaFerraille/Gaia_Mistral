import os
import sys
from datetime import datetime
from pathlib import Path

import gradio as gr
import plotly.graph_objects as go
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from mistralai.client import ChatMessage, MistralClient

# create a FastAPI app
app = FastAPI()

# create a static directory to store the static files
static_dir = Path('./static')
static_dir.mkdir(parents=True, exist_ok=True)

# mount FastAPI StaticFiles server
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Gradio stuff


# def predict(text_input):
#     file_name = f"{datetime.utcnow().strftime('%s')}.html"
#     file_path = static_dir / file_name
#     print(file_path)
#     with open(file_path, "w") as f:
#         f.write(f"""
#         <script src="https://cdn.tailwindcss.com"></script>
#         <body class="bg-gray-200 dark:text-white dark:bg-gray-900">
#         <h1 class="text-3xl font-bold">
#         Hello <i>{text_input}</i> From Gradio Iframe
#         </h1>
#         <h3>Filename: {file_name}</h3>
#         """)
#     iframe = f"""<iframe src="/static/{file_name}" width="100%" height="500px"></iframe>"""
#     link = f'<a href="/static/{file_name}" target="_blank">{file_name}</a>'
#     return link, iframe


# with gr.Blocks() as block:
#     gr.Markdown("""
# ## Gradio + FastAPI + Static Server
# This is a demo of how to use Gradio with FastAPI and a static server.
# The Gradio app generates dynamic HTML files and stores them in a static directory. FastAPI serves the static files.
# """)
#     with gr.Row():
#         with gr.Column():
#             text_input = gr.Textbox(label="Name")
#             markdown = gr.Markdown(label="Output Box")
#             new_btn = gr.Button("New")
#         with gr.Column():
#             html = gr.HTML(label="HTML preview", show_label=True)

#     new_btn.click(fn=predict, inputs=[text_input], outputs=[markdown, html])



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
        ),
        )

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



# mount Gradio app to FastAPI app
app = gr.mount_gradio_app(app, demo, path="/")

# serve the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
