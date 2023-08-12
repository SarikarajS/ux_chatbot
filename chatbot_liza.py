import openai
import gradio
import config_data
import logging

logging.basicConfig(level=logging.INFO, filename='app.log',
                    filemode='w', format='%(name)s - %(levelname)s - %(message)s')
  
openai.api_key = config_data.openapi_key

messages = [{"role": "system",
             "content": "You are a helpful customer care assistant for an e-commerce website dealing with complaints from users. Please only answer complaint-related queries."}]

def custom_chatGPT(user, name):
    messages.append({"role": "user", "content": user})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    logging.info(response, messages)

    chatGPT_reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": chatGPT_reply})
    return f"{name}: {chatGPT_reply}"


def message_and_history(input, history):
    history = history or []
    chat_history = list(sum(history, ()))
    chat_history.append(input)
    input_chats = ' '.join(chat_history)
    output = custom_chatGPT(input_chats, "Liza")
    history.append((input, output))
    return history, history


block = gradio.Blocks(title="AI Chatbot", theme='HaleyCH/HaleyCH_Theme')
with block:
    with gradio.Row():
        with gradio.Column():
            gradio.HTML("""""")
        with gradio.Column():
            with gradio.Row():
                chatbot = gradio.Chatbot()
            with gradio.Row():
                message = gradio.Textbox(placeholder="type here", label="Let's chat")
                state = gradio.State()
                message.submit(message_and_history,
                            inputs=[message, state],
                            outputs=[chatbot, state])
                message.submit(lambda x: gradio.update(value=''), [], [message])
        with gradio.Column():
            gradio.HTML("""
            <div style="display: flex; justify-content: center; margin-top: 20px;">
            <img src='/file=assets/images/female.jpg' style='width: 150px; height: 190px;'>
            </div>
            <h1 style="text-align: center;">Liza</h1>
            <h2 style="text-align:center;">Customer Service Assistant</h2>
            """)
        with gradio.Column():
            gradio.HTML("""""")


block.launch(debug=True, share=True)
