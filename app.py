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
from pydantic import BaseModel
from fastapi import Depends
import json
from fastapi.responses import HTMLResponse


# Load environment variables
load_dotenv()
api_key = os.getenv('API_KEY')
client = MistralClient(api_key=api_key)
model = 'mistral-small'

title = "Gaia Mistral Chat Demo"
description = "Example of simple chatbot with Gradio and Mistral AI via its API"
placeholder = "Posez moi une question sur l'agriculture"
examples = ["Comment fait on pour produire du maïs ?",
            "Rédige moi une lettre pour faire un stage dans une exploitation agricole", "Comment reprendre une exploitation agricole ?"]


# create a FastAPI app
app = FastAPI()

# create a static directory to store the static files
static_dir = Path('./static')
static_dir.mkdir(parents=True, exist_ok=True)

# mount FastAPI StaticFiles server
app.mount("/static", StaticFiles(directory=static_dir), name="static")


# Gradio stuff

def predict(text_input):
    file_name = f"{datetime.utcnow().strftime('%s')}.html"
    file_path = static_dir / file_name
    print(file_path)
    with open(file_path, "w") as f:
        f.write(f"""
        <script src="https://cdn.tailwindcss.com"></script>
        <body class="bg-gray-200 dark:text-white dark:bg-gray-900">
        <h1 class="text-3xl font-bold">
        Hello <i>{text_input}</i> From Gradio Iframe
        </h1>
        <h3>Filename: {file_name}</h3>
        """)
    iframe = f"""<iframe src="/static/{file_name}" width="100%" height="500px"></iframe>"""
    link = f'<a href="/static/{file_name}" target="_blank">{file_name}</a>'
    return link, iframe


with gr.Blocks() as block:
    gr.Markdown("""
## Gradio + FastAPI + Static Server
This is a demo of how to use Gradio with FastAPI and a static server.
The Gradio app generates dynamic HTML files and stores them in a static directory. FastAPI serves the static files.
""")
    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(label="Name")
            markdown = gr.Markdown(label="Output Box")
            new_btn = gr.Button("New")
        with gr.Column():
            html = gr.HTML(label="HTML preview", show_label=True)

    new_btn.click(fn=predict, inputs=[text_input], outputs=[markdown, html])


def create_world_map(lat, lon):

    fig = go.Figure(go.Scattermapbox(
        lat=[lat],
        lon=[lon],
        mode='markers',
        marker=go.scattermapbox.Marker(size=14),
        text=['Location'],
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


# # Fake JSON data for the user profile
# user_profile_data = {
#     "name": "John Doe",
#     "age": 30,
#     "location": "Montreal",
#     "lat": 45.5017,
#     "lon": -73.5673
# }

# #as a JSON:
# with open('user_profile.json', 'w') as f:
#     json.dump(user_profile_data, f)

# Mistral AI Chat

def chat_with_mistral(user_input):
    messages = [ChatMessage(role="user", content=user_input)]

    chat_response = client.chat(model=model, messages=messages)
    return chat_response.choices[0].message.content


### FRONTEND ###
def create_gradio_dashboard():
    with gr.Blocks() as demo:
        # Mistral AI Chat
        with gr.Column():
            with gr.Row():
                user_input = gr.Textbox (lines=2, placeholder=placeholder)
                send_chat_btn = gr.Button(value="Send")
                update_map_btn = gr.Button(value="Update Map")
            chat_output = gr.Textbox(lines=2, placeholder="Réponse")

        # Profile
        with gr.Row():
            name = gr.Textbox(label="Name")
            age = gr.Number(label="Age")
            location = gr.Textbox(label="Location")
            lat = gr.Number(value=45.5017, label="Latitude")
            lon = gr.Number(value=-73.5673, label="Longitude")
            load_user_profile_btn = gr.Button(value="Load User Profile")
            save_user_profile_btn = gr.Button(value="Save User Profile")

        # Map
        with gr.Row():
            map = gr.Plot()

        # Mistral AI Chat
        demo.load(chat_with_mistral, user_input, chat_output)
        send_chat_btn.click(chat_with_mistral, user_input, chat_output)

    return demo


# Profile stuff
class UserProfile(BaseModel):
    name: str
    age: int
    location: str
    lat: float
    lon: float

@app.post("/user_profile")
def save_user_profile(user_profile: UserProfile):
    with open('user_profile.json', 'w') as f:
        json.dump(user_profile.dict(), f)
    return user_profile.dict()

@app.get("/user_profile")
def load_user_profile():
    with open('user_profile.json', 'r') as f:
        user_profile = json.load(f)
    return UserProfile(**user_profile)

@app.put("/user_profile")
def update_user_profile(user_profile: UserProfile):
    with open('user_profile.json', 'w') as f:
        json.dump(user_profile.dict(), f)
    return user_profile

# load user profile on startup
user_profile = load_user_profile()


### BACKEND ###
@app.get("/meteo")
async def read_meteo(location: str, date: str):
    # API call to get the weather
    pass

# Home page : using the user profile, display the weather and chat with Mistral AI
@app.get("/", response_class=HTMLResponse)
async def home(user_profile: UserProfile = Depends(load_user_profile)):

    #1st : display as background the map of the user location:
    # get the user location
    lat = user_profile.lat
    lon = user_profile.lon
    # create the map
    fig = create_world_map(lat, lon)
    # save the map as a file
    map_file = static_dir / "map.html"
    fig.write_html(str(map_file))
    # display the map
    map_html = f'<iframe src="/static/map.html" width="100%" height="500px"></iframe>'

    #2nd : gradio dashboard on top of the map to toggle the user profile and display chat with Mistral AI
    # create the gradio dashboard
    # gradio_dashboard = create_gradio_dashboard()
    # save the dashboard as a file
    # dashboard_file = static_dir / "dashboard.html"
    # gradio_dashboard.save(dashboard_file)
    # # display the dashboard
    # dashboard_html = f'<iframe src="/static/dashboard.html" width="100%" height="500px"></iframe>'

    return f"""
    <h1>Welcome to the home page</h1>
    <h2>User Profile</h2>
    <p>Name: {user_profile.name}</p>
    <p>Age: {user_profile.age}</p>
    <p>Location: {user_profile.location}</p>
    <p>Latitude: {user_profile.lat}</p>
    <p>Longitude: {user_profile.lon}</p>
    <h2>Map</h2>
    {map_html}
    """
    # <h2>Gradio Dashboard</h2>
    # {dashboard_html}
