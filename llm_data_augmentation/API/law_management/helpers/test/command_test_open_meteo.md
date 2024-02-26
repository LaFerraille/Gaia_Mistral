curl "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"  


Lyon = 45.763420, 4.834277
curl "https://api.open-meteo.com/v1/forecast?latitude=45.763420&longitude=4.834277&current_weather=true" | jq '.current_weather'


Paris = 48.8566, 2.3522
curl "https://api.open-meteo.com/v1/forecast?latitude=48.8566&longitude=2.3522&current_weather=true" | jq '.current_weather'

