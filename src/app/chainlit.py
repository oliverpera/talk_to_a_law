import chainlit as cl
from replicate import Client
from chainlit.input_widget import Slider, Select, TextInput
from model_types import init_modeltypes
from configuration import UserConfiguration
import os
from embeddings import SpacyEmbeddingsFunction
from prompt_templates import prompt_template
from sqllite3_script import get_users
from sqllite3_script import check_user
import chromadb
from chainlit import User
from dotenv import load_dotenv


## global variables
config = UserConfiguration(None, None, None, None, None)
models = init_modeltypes()
users = [User(identifier="admin", metadata={"role": "admin", "provider": "credentials"})]


chroma_client = chromadb.PersistentClient(path="../resources/chromadb")
collection = chroma_client.get_collection(
        name="char_splitter_128_o0",
        embedding_function=SpacyEmbeddingsFunction(),
        # metadata={"hnsw:space": "cosine"} # "l2" (default: squared L2 norm), "ip" or "cosine"
)

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

def hide_api_key(api_key):
    return api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:]


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
    
    chroma_client = chromadb.PersistentClient(path="../resources/chromadb")

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
                initial=hide_api_key(load_replicate_key_from_env(user.identifier))
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



def check_if_replicate_api_key_is_set():
    print(config.get_replicate_api_key())
    if config.get_replicate_api_key() is None or config.get_replicate_api_key() == "":
        return False
    
    return True

@cl.on_settings_update
async def setup_agent(settings):
    print("Setup agent with following settings: ", settings)
    update_config(settings)

    ##cl.user_session.set("admin", user)

def set_prompt(message: cl.Message):
    query_result = collection.query(
        # query_embeddings=[], # embedded question / part of question # HERE: PREFORMULATE ANSWER, EMBED ANSWER, RETRIEVE REAL KNOWLEDGE ?!? # needs to be the same dimension as embedded vectors in db
        query_texts=[message.content], # ALTERNATIVE THAN QUERYING WITH EMBEDDINGS -> CHROMA WILL AUTOMATICALLY EMBED USING EMBEDDING FUNCTION OF COLLECTION
        n_results=4, # number of docs to retrieve
        # where={"metadata_field": "is_equal_to_this"}, # filter metadata
        # where_document={"$contains": "search_string"}, # filter for hard words / regexes etc.
        # include=["documents"], # specify which data to return (embeddings is excluded by default)
    )
    
    documents = query_result['documents']
    prompt = prompt_template.format(query=message.content, context=str(documents))
    return prompt

@cl.on_message
async def on_message(message: cl.Message):
    user = cl.user_session.get("user")
    msg = cl.Message(content="")
    
    if not check_if_replicate_api_key_is_set():
        config.set_replicate_api_key(hide_api_key(load_replicate_key_from_env(user.identifier)))

    prompt = set_prompt(message)
    
    replicateSession = Client(api_token=load_replicate_key_from_env(user.identifier))
        
    input = {
        "prompt": prompt,
        "max_new_tokens": 1024,
        "system_prompt": config.get_textinput(),
        "temperature": config.get_temperature(),
    }
        
    for event in replicateSession.stream(
        config.get_modelpath(),
        input=input,
        stream=True
    ):
        print(event, end="")
        await msg.stream_token(str(event))
        
    # msg = cl.Message(content=str(event))
    # await msg.send()
    # get_users()
    

def load_replicate_key_from_env(username):
    load_dotenv()
    username = username.upper()
    return os.getenv(f"{username}_API_KEY")
    
    
@cl.password_auth_callback
def auth_callback(username: str, password: str):
    global users
    if check_user(username,password):
        for user in users:
            if user.identifier == username:
                return user
            else:
                user = User(identifier=username, metadata={"role": "admin", "provider": "credentials"})
                users.append(user)
                return user
    else:
        print("User not found")
        return None

 
 
    
    
