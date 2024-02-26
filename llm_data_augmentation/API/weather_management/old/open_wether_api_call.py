import requests

# Define the URL with the query parameters for latitude and longitude, and the metrics you want to retrieve
url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current_weather=true&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"

# Make the HTTP GET request to the Open-Meteo API
response = requests.get(url)

# Parse the JSON response
weather_data = response.json()

# Print the current weather, for example
current_weather = weather_data.get('current_weather', {})
print(f"Current temperature: {current_weather.get('temperature')}°C")
print(f"Current wind speed: {current_weather.get('windspeed')} km/h")

# If you also want to print a bit of the hourly forecast
hourly_forecast = weather_data.get('hourly', {})
times = hourly_forecast.get('time', [])[:5]  # Just an example to get the first 5 time points
temperatures = hourly_forecast.get('temperature_2m', [])[:5]
print("\nHourly forecast (first 5 hours):")
for time, temp in zip(times, temperatures):
    print(f"{time}: {temp}°C")
