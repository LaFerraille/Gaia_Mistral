from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from dotenv import load_dotenv
import os
from .helpers.check_pesticide_approval import check_pesticide_approval


# Load environment variables
load_dotenv()

# Mistral AI client setup
api_key = os.getenv('API_KEY')
client = MistralClient(api_key=api_key)
model="mistral-medium"


def answer_question_about_weather(user_question):
    approval = check_pesticide_approval(user_question)
    return approval


if __name__ == "__main__":
    user_question = "Fenhexamid"
    answer = answer_question_about_weather(user_question)
    print(f'Answer to "{user_question}": {answer}')


