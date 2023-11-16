from model import execute_bot
import chainlit as cl

@cl.on_chat_start
async def start():
    chain = execute_bot()
    msg = cl.Message(content="Starting the bot...")
    await msg.send()
    msg.content = "Hallo und willkommen bei FinBot. Wie kann ich Dir helfen?"
    await msg.update()

    cl.user_session.set("chain", chain)

@cl.on_message
async def main(message: cl.Message):
    chain = cl.user_session.get("chain") 
    
    cb = cl.AsyncLangchainCallbackHandler(
        stream_final_answer=True, answer_prefix_tokens=["FINAL", "ANSWER"]
    )
    cb.answer_reached = True
    
    res = await cl.make_async(chain)(message, callbacks=[cb])

    answer = res["result"]
    sources = res["source_documents"]

    if sources:
        answer += f"\nSources:" + str(sources)
    else:
        answer += "\nNo sources found"

    await cl.Message(content=answer).send()
