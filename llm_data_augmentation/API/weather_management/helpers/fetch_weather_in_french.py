import requests

# Function to fetch weather data from Open-Meteo and format it in French
def fetch_weather_in_french(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url)
    weather_data = response.json()
    current_weather = weather_data.get('current_weather', {})
    temperature = current_weather.get('temperature')
    windspeed = current_weather.get('windspeed')
    return f"La température actuelle est de {temperature}°C avec une vitesse du vent de {windspeed} km/h."

