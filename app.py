import os
import sys
from datetime import datetime
from pathlib import Path
import plotly.graph_objects as go
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from mistralai.client import ChatMessage, MistralClient
from pydantic import BaseModel
from fastapi import Depends
import json
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from datetime import date
from weather import get_weather

# code that gives the date of today
today = date.today()
today = today.strftime("%Y-%m-%d")


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


def chat_with_mistral(user_input):
    messages = [ChatMessage(role="user", content=user_input)]

    chat_response = client.chat(model=model, messages=messages)
    return chat_response.choices[0].message.content




# Profile stuff
class UserProfile(BaseModel):
    name: str
    age: int
    location: str
    lat: float
    lon: float

class UserLocation(BaseModel):
    city: str

class Weather(BaseModel):
    temperature: float
    humidity: float
    pression: float



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

@app.get("/weather")
def load_weather():
    with open('Weather.json', 'r') as f:
        w = json.load(f)
    return Weather(**w)


# @app.post("/user_location")
# async def set_user_location(user_location: UserLocation):
#     # Save the user location as a JSON file
#     with open('user_location.json', 'w') as f:
#         json.dump(user_location.dict(), f)
#     return RedirectResponse(url='/home')

@app.post("/user_location")
async def set_user_location(user_location: UserLocation):
    # Save the user location as a JSON file
    with open('user_location.json', 'w') as f:
        json.dump(user_location.dict(), f)
    response = Response(headers={"Location": "/home"})
    response.status_code = 303
    return response

# load user profile on startup
user_profile = load_user_profile()
weather=load_weather()

### BACKEND ###
@app.get("/meteo")
async def read_meteo(location: str, date: str):
    # API call to get the weather
    pass











# On récupère les infos sur la ville. On les sauvegarde dans un fichier JSON
@app.get("/", response_class=HTMLResponse)
async def enter_location():
    return """
    <form id="locationForm">
        <label for="city">Enter your city:</label><br>
        <input type="text" id="city" name="city"><br>
        <input type="submit" value="Submit">
    </form>
    <script>
    document.getElementById('locationForm').addEventListener('submit', function(event) {
        event.preventDefault();
        var city = document.getElementById('city').value;
        fetch('/user_location', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({city: city}),
        })
        .then(response => {
            if (response.redirected) {
                window.location.href = '/home';
            }
        });
    });
    </script>
    """


# Home page : using the user profile, display the weather and chat with Mistral AI
@app.get("/home", response_class=HTMLResponse)
async def home(user_profile: UserProfile = Depends(load_user_profile), Weather: Weather = Depends(load_weather)):

    #1st : display as background the map of the user location:
    # get the user location
    lat = user_profile.lat
    lon = user_profile.lon
    temperature = Weather.temperature
    humidity = Weather.humidity
    pression = Weather.pression
    # create the map
    fig = create_world_map(lat, lon)
    # save the map as a file
    map_file = static_dir / "map.html"
    fig.write_html(str(map_file))
    # display the map
    map_html = f'<iframe src="/static/map.html" width="100%" height="500px"></iframe>'

    
    return f"""
        <center>
        <h1>Bienvenu !</h1></center>
        <div style="display: flex;">
            <div style="flex: 50%;">
                <h2>Informations du jour</h2>
                <p>temperature: {temperature}</p>
                <p>humidity: {humidity}</p>
                <p>pression: {pression}</p>
                <h2>Map</h2>
                {map_html}

            </div>
            <div style="flex: 50%;">
                <h2>Avez-vous une question ?</h2>
                <textarea style="width: 100%; height: 500px;"></textarea>
            </div>
        </div>
        """
    # <h2>Gradio Dashboard</h2>
    # {dashboard_html}
