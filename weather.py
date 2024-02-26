import requests
import json
import datetime
from pprint import pprint   
from datetime import date
def get_weather(city, date):
    agro_api_key = "88aaa872e29fedb008a2ffd240ebdf56"
    opencage_api_key = "bade196e8eac4d33b72dba6d9e40285a"

    # On récupère les lat et lon de la ville
    geocode_url = f"https://api.opencagedata.com/geocode/v1/json?q={city}&key={opencage_api_key}"
    geocode_response = requests.get(geocode_url)
    geocode_data = geocode_response.json()

    
    latitude = geocode_data['results'][0]['geometry']['lat']
    longitude = geocode_data['results'][0]['geometry']['lng']

    # On demande la météo pour cette ville
    forecast_url = f"http://api.agromonitoring.com/agro/1.0/weather/forecast?lat={latitude}&lon={longitude}&appid={agro_api_key}"
    forecast_response = requests.get(forecast_url)

    if forecast_response.status_code == 200:
        forecast_data = forecast_response.json()
        d={}
        for forecast in forecast_data:
            datew = datetime.datetime.fromtimestamp(forecast['dt'])
            temperature = forecast['main']['temp']
            weather_description = forecast['weather'][0]['description']

            if str(datew).split(' ')[0]==str(date) :
                d[str(datew)]=f"Location : {city}, Temperature: {round(temperature-273.15,2)}°C, Weather: {weather_description}"
        return d
    else:
        print(f"Error: {forecast_response.status_code}")

# #exemple
# today = date.today()
# today = today.strftime("%Y-%m-%d")
# a=get_weather('Paris',today)
# print(a)