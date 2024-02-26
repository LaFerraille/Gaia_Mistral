from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from dotenv import load_dotenv
import os
from .helpers.extract_city_name import extract_city_name
from .helpers.fetch_coordinates import fetch_coordinates
from .helpers.fetch_weather_in_french import fetch_weather_in_french

# Load environment variables
load_dotenv()

# Mistral AI client setup
api_key = os.getenv('API_KEY')
client = MistralClient(api_key=api_key)
model="mistral-medium"


def answer_question_about_weather(user_question):
    # Extract city name
    city_name = extract_city_name(user_question, api_key, model)
    # Fetch coordinates
    lat, lon = fetch_coordinates(city_name)
    # Prepare weather message in French
    weather_message = fetch_weather_in_french(lat, lon)
    return weather_message


if __name__ == "__main__":
    user_question = "Quelle est la météo à Livron aujourd'hui ?"
    answer = answer_question_about_weather(user_question)
    print(f'Answer to "{user_question}": {answer}')


