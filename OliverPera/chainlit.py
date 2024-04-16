from model import execute_bot
import chainlit as cl
from typing import Optional
##from chainlit.client.cloud import chainlit_client
##from chainlit.types import AppUser
# from create_appuser import create_new_user
import replicate
##from prompt_templates import PromptTemplate


@cl.password_auth_callback
def auth_callback(username: str, password: str) -> Optional[cl.AppUser]:
    username = 'admin'
    password = 'admin'
    
    if (username, password) == ("admin", "admin"):
        ##create_new_user()
    
        return cl.AppUser(username="admin", role="ADMIN", provider="credentials")
        
    else:
        return None

@cl.on_chat_start
async def start():
    ### = execute_bot("")
    msg = cl.Message(content="Starting the bot...")
    await msg.send()
    
    files = None
    while files is None:
        files = await cl.AskFileMessage(
            content="HALLO",
            accept=["application/pdf"],
            max_size_mb=20,
        ).send()
    file = files[0]

    # Process and save data in the user session
    msg = cl.Message(content=f"Processing `{file.name}`...")
    await msg.send()
    docs = file
    cl.user_session.set("docs", docs)
    msg.content = f"`{file.name}` processed. Loading ..."
    await msg.update()
    msg.content = "Hallo und willkommen bei FinBot. Wie kann ich Dir helfen?"
    await msg.update()
    

    cl.user_session.set("chain", "chain")

# @cl.on_message
# async def main(message: cl.Message):
#     chain = cl.user_session.get("chain") 
    
#     cb = cl.AsyncLangchainCallbackHandler(
#         stream_final_answer=True, answer_prefix_tokens=["FINAL", "ANSWER"]
#     )
#     cb.answer_reached = True
    
#     res = await cl.make_async(chain)(message, callbacks=[cb])

#     answer = res["result"]
#     sources = res["source_documents"]

#     if sources:
#         answer += f"\nSources:" + str(sources)
#     else:
#         answer += "\nNo sources found"

#     await cl.Message(content=answer).send()
    
    
    


@cl.on_message
async def on_message(message: cl.Message):    
    msg = cl.Message(content="")
    
    input = {
        "prompt": message,
        "max_new_tokens": 1024,
        "system_prompt": "Du bist ein hilfsbereiter, freundlicher und verständlicher Assistent. Du hast Zugriff auf eine Wissensdatenbank für das Deutsche Bankrecht und kannst Fragen beantworten."
    }
    
    for event in replicate.stream(
        "mistralai/mixtral-8x7b-instruct-v0.1",
        input=input,
        stream=True
    ):
        print(event, end="")
        await msg.stream_token(str(event))

    await msg.send()
    
    

