# from model import execute_bot
# from chainlit.client.cloud import chainlit_client
# from chainlit.types import AppUser
# from create_appuser import create_new_user
# from typing import Optional
# from chainlit.client.base import AppUser, PersistedAppUser


import chainlit as cl
import replicate
from chainlit.input_widget import Slider, Select, TextInput
from model_types import init_modeltypes
from configuration import UserConfiguration
import os

config = UserConfiguration(None, None, None, None, None)
models = init_modeltypes()


def update_config(settings):
    config.set_temperature(settings["Temperature"])
    config.set_select(settings["Model"])
    config.set_modelpath(get_modelpath(settings["Model"]))
    config.set_replicate_api_key(settings["ReplicateAPIKey"])
    config.set_textinput(settings["SystemPrompt"])
    
    print(config.get_temperature(), config.get_select(), config.get_modelpath(), config.get_textinput())


def get_modelpath(model_id):
    for model in models:
        if model.id == model_id:
            return model.name
    return None


async def accept_file():
    files = None
    while files is None:
        files = await cl.AskFileMessage(
            content="HALLO",
            accept=["application/pdf"],
            max_size_mb=20,
        ).send()
    file = files[0]

    msg = cl.Message(content=f"Processing `{file.name}`...")
    await msg.send()
    docs = file
    cl.user_session.set("docs", docs)
    msg.content = f"`{file.name}` processed. Loading ..."
    await msg.update()



@cl.on_chat_start
async def start():    
    user = cl.user_session.get("user")
    msg = cl.Message(content="Starting the bot...")
    await msg.send()
    
    settings = await cl.ChatSettings(
        [
            Slider(
                id="Temperature",
                label="Temperature",
                initial=1,
                min=0,
                max=2,
                step=0.1,
            ),
            Select(
                id="Model",
                label="Large Language Model",
                values=[model.id for model in init_modeltypes()],
                initial_index=0,
            ),
            TextInput(
                id="ReplicateAPIKey",
                label="Replicate API Key",
                initial="XXX-YYY-ZZZ"
            ),
            TextInput(
                id="SystemPrompt", 
                label="System Prompt", 
                initial="Du bist ein hilfsbereiter, freundlicher und verständlicher Assistent. Du hast Zugriff auf eine Wissensdatenbank für das Deutsche Bankrecht und kannst Fragen beantworten.")
        ]
    ).send()
    
    msg.content = "Hallo und willkommen bei FinBot. Wie kann ich Dir helfen?"
    await msg.update()
    
    update_config(settings)
    
    cl.user_session.set("user", user)


@cl.on_stop
def on_stop():
    print("The user wants to stop the task!")


@cl.on_settings_update
async def setup_agent(settings):
    print("Setup agent with following settings: ", settings)
    update_config(settings)

    ##cl.user_session.set("admin", user)

@cl.on_message
async def on_message(message: cl.Message):    
    counter = cl.user_session.get("admin")
    msg = cl.Message(content="")
        
    input = {
        "prompt": str(message),
        "max_new_tokens": 1024,
        "system_prompt": config.get_textinput(),
        "temperature": config.get_temperature(),
    }
        
    for event in replicate.stream(
        config.get_modelpath(),
        input=input,
        stream=True
    ):
        print(event, end="")
        await msg.stream_token(str(event))
        
    # answers = replicate.run(
    #     config.get_modelpath(),
    #     input=input
    # )
    # print(answers)
    
    # output = ''
    # for answer in answers:
    #     output += answer
    
    # msg = cl.Message(content=output)

    await msg.send()
    
    
    
### chainlit bug: https://github.com/Chainlit/chainlit/issues/864
# @cl.password_auth_callback
# def auth_callback(username: str, password: str) -> Optional[cl.User]:
#     if (username, password) == ("admin", "admin"):
#         return cl.User(identifier="admin")
#     else:
#         return None



