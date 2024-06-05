import requests

class LLMModelType:
    def __init__(self, id, name):
        self.id = id
        self.name = name


def get_model_types():
    try:
        ## run locally without docker 
        ## response = requests.get("http://localhost:1234/v1/models") ## default API Endpoint for LM Studio
        response = requests.get("http://host.docker.internal:1234/v1/models") ## default API Endpoint for LM Studio
        return extract_models(response.json())
    
    except requests.exceptions.RequestException as e:
        errorMsg = f"\033[1;31mError: Failed to establish connection to local LM Studio API. Please check if the Server is running. \nError Message: {e}\033[0m"
        raise RuntimeError(errorMsg)
        

def extract_models(json_response):
    models = []
    
    for item in json_response['data']:
        models.append(item['id'])
    
    return models

            
def init_modeltypes():
    model_types = []    
    models = get_model_types()
    
    if models is None:
        return None
    
    count = 0
    for model in models:
        count += 1
        model_types.append(LLMModelType(f"LLM {count}: {model}", model))

    return model_types

# for model in init_modeltypes():
#     print(model.id, model.name)    