import requests

# Function to fetch coordinates using Open Street Map API
def fetch_coordinates(city_name):
    osm_url = f"https://nominatim.openstreetmap.org/search?city={city_name}&format=json"
    response = requests.get(osm_url)
    data = response.json()
    lat = data[0]['lat']
    lon = data[0]['lon']
    return lat, lon
