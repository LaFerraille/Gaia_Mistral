from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from dotenv import load_dotenv
import os

def choose_api(question, api_key, model="mistral-medium"):
    prompt = f"Given the question: '{question}' if you judge it would be useful to include data from one the following database: [current weather, animal medecines], just return the name of each database under a list format, do not return anything else in any case "

    client = MistralClient(api_key=api_key)
    messages = [
        ChatMessage(role="user", content=prompt)
    ]

    chat_response = client.chat(
        model=model,
        messages=messages,
    )

    return(chat_response.choices[0].message.content)


if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv('API_KEY')
    client = MistralClient(api_key=api_key)
    model="mistral-medium"
    api_needed = choose_api('quel medicament dois-je utiliser pour une vache malade selon la meteo de ce soir ?', api_key, model)
    print(f'API needed for the question: {api_needed}')
