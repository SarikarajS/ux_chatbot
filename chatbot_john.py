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


block = gradio.Blocks(title="AI Chatbot", theme=gradio.themes.Monochrome())
with block:
    gradio.HTML("""
    <div style="text-align:center;">
        <h1>Customer Service Assistant</h1>
    </div>
    """)
    with gradio.Row():
        message = gradio.Textbox(placeholder="type here", label="Let's chat")
        chatbot = gradio.Chatbot()
        state = gradio.State()
        message.submit(message_and_history,
                       inputs=[message, state],
                       outputs=[chatbot, state])
        message.submit(lambda x: gradio.update(value=''), [], [message])

        gradio.HTML("""
        <div style="display: flex; justify-content: center; margin-top: 20px;">
        <img src='/file=assets/images/male.JPG' style='width: 160px; height: 190px;'>
        </div>
        <h2 style="text-align: center;">Liza</h2> 
        """)


block.launch(debug=True, share=True)