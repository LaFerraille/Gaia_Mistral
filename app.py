import gradio as gr

def answer_question(question):
    # This is a placeholder function. You should implement your model inference logic here.
    # For demonstration purposes, we'll return a generic answer.
    answers = {
        "how to detect crop disease": "To detect crop diseases, use image recognition models trained on datasets of diseased and healthy crops.",
        "best time to plant wheat": "The best time to plant wheat depends on your region. In temperate regions, it's usually early autumn.",
        "improving soil fertility": "Improving soil fertility can be achieved by rotating crops, using compost, and avoiding overuse of chemical fertilizers.",
    }
    # Find the closest question and return the answer
    question = question.lower()
    for key in answers:
        if key in question:
            return answers[key]
    return "I'm not sure how to answer that. Can you ask something else?"

app = gr.Interface(fn=answer_question,
                   inputs=gr.inputs.Textbox(lines=2, placeholder="Ask a question about agriculture..."),
                   outputs="text",
                   title="Agriculture Assistant",
                   description="Ask any question about agriculture, and I'll try to provide an informative answer.")

if __name__ == "__main__":
    app.launch()
