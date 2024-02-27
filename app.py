import json
import os
from datetime import date, datetime
from pathlib import Path

import plotly.graph_objects as go
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from mistralai.client import ChatMessage, MistralClient
from pydantic import BaseModel

from weather import get_weather

# code that gives the date of today
today = date.today()
today = today.strftime("%Y-%m-%d")


# Hugging face space secret retrieval:
def create_env_file():
    import os

    secrets = ['MISTRAL_API_KEY', 'AGRO_API_KEY', 'OPENCAGE_API_KEY']
    for secret in secrets:
        secret_value = os.environ[secret]
        if secret_value is None:
            print(f"Please set the environment variable {secret}")
        else:
            with open('.env', 'a') as f:
                f.write(f"{secret}={secret_value}\n")


# Hugging face space secret retrieval:
production = True
if production:
    create_env_file()


# Load environment variables
load_dotenv()
api_key = os.getenv('MISTRAL_API_KEY')
client = MistralClient(api_key=api_key)
model = 'mistral-small'

title = "Gaia Mistral Chat Demo"
description = "Example of simple chatbot with Gradio and Mistral AI via its API"
placeholder = "Posez moi une question sur l'agriculture"
examples = ["Comment fait on pour produire du maïs ?",
            "Rédige moi une lettre pour faire un stage dans une exploitation agricole", "Comment reprendre une exploitation agricole ?"]


def create_prompt_system():

    prompt = "Ton rôle: Assistant agricole\n\n"

    prompt += "Ton objectif: Aider les agriculteurs dans leur recherche d'information. Tu peux répondre à des questions sur l'agriculture, donner des conseils, ou aider à rédiger des documents administratifs.\n\n"

    prompt += "Ton public: Agriculteurs, étudiants en agriculture, personnes en reconversion professionnelle, ou toute personne ayant des questions sur l'agriculture.\n\n"

    prompt += "Ton style: Tu es professionnel, bienveillant, et tu as une connaissance approfondie de l'agriculture. Tu réponds uniquement en français et de manière semi-concise. Tu es capable de répondre à des questions techniques, mais tu sais aussi t'adapter à des personnes qui ne connaissent pas bien le domaine.\n\n"

    prompt += "Tu disposes du contexte suivant pour répondre aux questions:\n\n"

    # load all the json files in the root
    for file in Path('.').glob('*.json'):
        with open(file, 'r') as f:
            prompt += f"Contexte: {file.stem}\n\n"
            # convert the json to a string using the json module
            file_content = json.load(f)
            prompt += json.dumps(file_content, indent=4)
            prompt += "\n\n"

    prompt += "Tu es prêt à répondre aux questions ?\n\n"
    return prompt


def chat_with_mistral(user_input):
    messages = [ChatMessage(role="user", content=user_input)]

    chat_response = client.chat(model=model, messages=messages)
    return chat_response.choices[0].message.content


# create a FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
# create a static directory to store the static files
static_dir = Path('./static')
static_dir.mkdir(parents=True, exist_ok=True)

# mount FastAPI StaticFiles server
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# templating
templates = Jinja2Templates(directory="static")

with open('data/departements.geojson', 'r') as f:
    departements = json.load(f)

with open('data/regions.geojson', 'r') as f:
    regions = json.load(f)


def create_world_map(lat, lon, dpmts=False, rgns= False):

    fig = go.Figure()

    if dpmts :
        for feature_departement in departements['features']:
            if feature_departement['geometry']['type'] == 'Polygon':
                coords = feature_departement['geometry']['coordinates'][0]
                lons, lats = zip(*coords)
                lons = list(lons)
                lats = list(lats)
                fig.add_trace(go.Scattermapbox(
                    mode='lines',
                    lon=lons + [lons[0]],
                    lat=lats + [lats[0]],
                    marker=go.scattermapbox.Marker(
                        size=14
                    ),
                    text=feature_departement['properties']['nom'],
                    hoverinfo='text',
                    line=dict(
                        color='blue',
                        width=1
                    ),
                    showlegend=False,
                    visible=True,
                ))

    if rgns:
        for feature_region in regions['features']:
            if feature_region['geometry']['type'] == 'Polygon':
                coords = feature_region['geometry']['coordinates'][0]
                lons, lats = zip(*coords)
                lons = list(lons)
                lats = list(lats)
                fig.add_trace(go.Scattermapbox(
                    mode='lines',
                    lon=lons + [lons[0]],
                    lat=lats + [lats[0]],
                    hoverinfo='text',
                    line=dict(
                        color='red',  # Set the line color to red
                        width=1,  # Set the width of the line
                    ),
                    showlegend=False,
                    visible=True,
                ))

    fig.add_trace(go.Scattermapbox(
        lat=[lat],
        lon=[lon],
        mode='markers',
        marker=go.scattermapbox.Marker(size=14, color='red'),
        text=['Location'],
        showlegend=False,
        hoverinfo='none'
    ))

    fig.update_layout(
        autosize=True,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
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
    weather: str


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

# Load user location


def load_user_location():
    with open('user_location.json', 'r') as f:
        user_location = json.load(f)
    return UserLocation(**user_location)

# Save weather information


def save_weather(weather: Weather):

    with open('Weather.json', 'w') as f:
        json.dump(weather.dict(), f)


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
weather = load_weather()


@app.get("/", response_class=HTMLResponse)
async def enter_location():
    return """
    <html>
    <head>
        <style>
            body {
                background-image: url('static/background.png');
                background-size: cover;
                color: white; /* make all the text white */
                font-size: 20px; /* increase the font size */
                font-family: sans-serif; /* change the font to Arial */
            }
            img {
                display: block;
                margin-left: auto;
                margin-right: auto;
                width: 50%;
            }
            input[type="text"], input[type="submit"] {
                width: 100%;
                padding: 10px 20px;
                margin: 10px 0;
                box-sizing: border-box;
                border: none;
                border-radius: 4px;
                background-color: #f8f8f8;
                font-size: 16px;
            }
        </style>
    </head>
    <body>
        <img src="static/mistral.png" alt="Mistral Logo" style="display: block; margin-left: auto; margin-right: auto; width: 50%;">
        <h2>Bienvenue sur votre AI-dashboard connecté</h2>
        <p>Connectez-vous et accédez à des informations personnalisées !</p>

        <h2> Fonctionnalités</h2>
        <ul>
            <li> Parlez avec votre assistant Mistral</li>
            <li> Obtenez des renseignements météo</li>
            <li> Partagez des informations avec les agriculteurs de votre région </li>
            <li> Générer une newsletter personnalisée grâce à Mistral</li>
        </ul>
        
        <form id="locationForm">
            <label for="city">Votre ville :</label><br>
            <input type="text" id="city" name="city"><br>
            <input type="submit" value="Submit">
        </form>
        <div>
            <p>© 2024 AgriHackteurs</p>
        </div>
    </body>
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
            if (response.ok) {
                window.location.href = "/home";
            }
        });
    });
    </script>
    """


# Home page : using the user profile, display the weather and chat with Mistral AI
@app.get("/home", response_class=HTMLResponse)
async def home(
    request: Request,
    user_profile: UserProfile = Depends(load_user_profile),
    weather: Weather = Depends(load_weather),
):

    with open('user_location.json', 'r') as f:
        user_location = json.load(f)
    # Get weather data for the user location
    weather_data, lat, lon = get_weather(user_location['city'], today)
    # Convert the keys to datetime objects
    weather_times = {datetime.strptime(
        time, '%Y-%m-%d %H:%M:%S'): info for time, info in weather_data.items()}
    # Find the time closest to the current time
    current_time = datetime.now()
    closest_time = min(weather_times.keys(),
                       key=lambda time: abs(time - current_time))
    # Extract weather information for the closest time
    weather_info = weather_times[closest_time]
    # Extract temperature and weather from the weather information
    temperature = float(weather_info.split(
        ', ')[1].split('°C')[0].split(': ')[1])
    weather = weather_info.split(', ')[2].split(': ')[1]
    # Create a Weather object from the weather data
    weather = Weather(temperature=temperature, weather=weather)
    temperature = weather.temperature
    weather = weather.weather

    # create the map
    fig = create_world_map(lat, lon, dpmts=True, rgns=True)
    # save the map as a file
    map_file = static_dir / "map.html"
    fig.write_html(str(map_file), config={'displayModeBar': False})
    # display the map
    map_html = f'<iframe src="/static/map.html" width="100%" height="100%" ></iframe>'

    # initialize the chatbot with the system prompt
    system_prompt = create_prompt_system()
    chat_with_mistral(system_prompt)


    return templates.TemplateResponse("layout.html", {"request": request, "user_profile": user_profile, "weather": weather, "map_html": map_html})


class ChatInput(BaseModel):
    user_input: str


@app.post("/chat")
async def chat(chat_input: ChatInput):
    print(chat_input.user_input)
    return chat_with_mistral(chat_input.user_input)

# summarize all the information from the json files


@app.get("/report")
async def report():
    # load all the json files in the root
    report = ""
    for file in Path('.').glob('*.json'):
        with open(file, 'r') as f:
            report += f"Contexte: {file.stem}\n\n"
            # convert the json to a string using the json module
            file_content = json.load(f)
            report += json.dumps(file_content, indent=4)
            report += "\n\n"

    report += "Synthétise les informations pour l'utilisateur : \n\n"
    # ask mistral to summarize the report
    chat_response = client.chat(model=model, messages=[
                                ChatMessage(role="user", content=report)])
    return chat_response.choices[0].message.content
