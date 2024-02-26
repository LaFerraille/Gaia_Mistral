# import gradio as gr
# from mistralai.client import MistralClient, ChatMessage
# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()
# api_key = os.getenv('API_KEY')

# # Initialize Mistral client with the API key
# client = MistralClient(api_key=api_key)

# def answer_question(question):
#     """Directly ask Mistral the question and return the answer."""
#     # Format the user's question for Mistral
#     user_message = question

#     # Use the run_mistral function to get an answer
#     answer = run_mistral(user_message)
    
#     return answer

# def run_mistral(user_message, model="mistral-medium"):
#     """Interact with Mistral using chat."""
#     messages = [ChatMessage(role="user", content=user_message)]
#     chat_response = client.chat(model=model, messages=messages)
#     return chat_response.choices[0].message.content

# app = gr.Interface(fn=answer_question,
#                    inputs=gr.inputs.Textbox(lines=2, placeholder="Ask a question..."),
#                    outputs="text",
#                    title="Your Assistant",
#                    description="Ask any question, and I'll try to provide an informative answer.")

# if __name__ == "__main__":
#     app.launch(share=True)  # Set `share=True` to create a public link
