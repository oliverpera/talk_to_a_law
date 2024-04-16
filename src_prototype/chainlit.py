import chainlit as cl
from model import execute_bot


@cl.on_chat_start
async def start():
    msg = cl.Message(content="Starting the bot...")
    chain = execute_bot("")
    await msg.send()
    msg.content = "Hallo und willkommen bei FinBot. Wie kann ich Dir helfen?"
    await msg.update()

    cl.user_session.set("chain", chain)

@cl.on_message
async def on_message(message: cl.Message):
    response = f"Hello, you just sent: {message}!"
    answer = execute_bot(str(message))
    
    await cl.Message(answer).send()
