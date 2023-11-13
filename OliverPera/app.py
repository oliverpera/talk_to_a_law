import chainlit as cl


@cl.on_message
async def main(message: cl.Message):
    # Your custom logic goes here...

    # Send a response back to the user
    await cl.Message(
        content="Received: {message.content}",
    ).send()
    await cl.Message(
        content="Hello",
    ).send()
