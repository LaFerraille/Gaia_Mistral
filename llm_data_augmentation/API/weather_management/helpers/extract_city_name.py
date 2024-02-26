from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


def extract_city_name(question, api_key, model="mistral-medium"):
    # Prepare the prompt for the LLM
    prompt = f"Given the question: '{question}', identify and extract the name of the city mentioned. Just return the name of the city."

    client = MistralClient(api_key=api_key)
    messages = [
        ChatMessage(role="user", content=prompt)
    ]

    # No streaming
    chat_response = client.chat(
        model=model,
        messages=messages,
    )

    return(chat_response.choices[0].message.content)
