import chainlit as cl
from chainlit.input_widget import Slider, Select, TextInput
from model_types import init_modeltypes
from configuration import UserConfiguration
from prompt_templates import prompt_template_zero_shot
import chromadb
from chainlit import User
from chromadb import Documents, EmbeddingFunction, Embeddings
import spacy
from openai import AsyncOpenAI

## global variables
config = UserConfiguration(None, None, None, None)
models = init_modeltypes()
users = [User(identifier="admin", metadata={"role": "admin", "provider": "credentials"})]

## run locally without docker 
##chroma_client = chromadb.PersistentClient(path="../resources/chromadb/")
chroma_client = chromadb.PersistentClient(path="../resources/chromadb")


def update_config(settings):
    config.set_temperature(settings["Temperature"])
    config.set_select(settings["Model"])
    config.set_modelpath(get_modelpath(settings["Model"]))
    config.set_textinput(settings["SystemPrompt"])
    
    print(config.get_temperature(), config.get_select(), config.get_modelpath(), config.get_textinput())


def get_modelpath(model_id):
    for model in models:
        if model.id == model_id:
            return model.name
    return None


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
                initial=0,
                min=0,
                max=2,
                step=0.1,
            ),
            Select(
                id="Model",
                label="LLM loaded from LM Studio",
                values=[model.id for model in init_modeltypes()],
                initial_index=0,
            ),
            # Since we are running the LLM locally there is no need to have the API key
            # TextInput(
            #     id="ReplicateAPIKey",
            #     label="Replicate API Key",
            #     initial=hide_api_key(load_replicate_key_from_env(user.identifier))
            # ),
            TextInput(
                id="SystemPrompt", 
                label="System Prompt", 
                initial="Du bist ein deutschsprachiger Assistent für das deutsche Bankenrecht. Beantworte die Anfrage des Nutzers in deutsch.")
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
    update_config(settings)
    print("Setup agent with following settings: ", settings)
    updateMsg = cl.Message(content=f"Settings updated: {settings}")
    await updateMsg.send()

def set_prompt(message: cl.Message):
    user = cl.user_session.get("user")

    class SpacyEmbeddingsFunction(EmbeddingFunction):
        def __call__(self, input: Documents) -> Embeddings:
            nlp = spacy.load("de_core_news_lg") # md , lg
            embeddings = [nlp(document).vector.tolist() for document in input]
            return embeddings
    
    collection = chroma_client.get_collection(
        name="char_splitter_1024_o128_spacy",
        embedding_function=SpacyEmbeddingsFunction()
        # metadata={"hnsw:space": "cosine"} # "l2" (default: squared L2 norm), "ip" or "cosine"
)
    query_result = collection.query(
        # query_embeddings=[], # embedded question / part of question # HERE: PREFORMULATE ANSWER, EMBED ANSWER, RETRIEVE REAL KNOWLEDGE ?!? # needs to be the same dimension as embedded vectors in db
        query_texts=[message.content], # ALTERNATIVE THAN QUERYING WITH EMBEDDINGS -> CHROMA WILL AUTOMATICALLY EMBED USING EMBEDDING FUNCTION OF COLLECTION
        n_results=2, # number of docs to retrieve
        # where={"metadata_field": "is_equal_to_this"}, # filter metadata
        # where_document={"$contains": "search_string"}, # filter for hard words / regexes etc.
        # include=["documents"], # specify which data to return (embeddings is excluded by default)
    )
    
    documents = query_result['documents']
    prompt = prompt_template_zero_shot.format(query=message.content, context=str(documents))
    return prompt

@cl.on_message
async def on_message(message: cl.Message):
    user = cl.user_session.get("user")
    msg = cl.Message(content="")
    
    prompt = set_prompt(message)
    
    client = AsyncOpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    cl.instrument_openai()
        
    try:
        stream = await client.chat.completions.create(
            model=config.get_modelpath(),   
            temperature=config.get_temperature(),
            messages=[{"role": "system", "content": config.get_textinput()},
                      {"role": "user", "content": prompt}],
            stream=True,
        )
        
        async for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content)
                await msg.stream_token(str(chunk.choices[0].delta.content))
            else:
                print("No content received. The response is empty.")
                errorMsg = cl.Message(content="No content received. The response is empty.")
                await errorMsg.send()
               
    except Exception as e:
        errorMsg = cl.Message(content=f"Error: Failed to establish connection: {e}")
        print("Error: Failed to establish connection: ", e)
        await errorMsg.send()
            
            

    
    
