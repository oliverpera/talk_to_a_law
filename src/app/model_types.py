class LLMModelType:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    
def init_modeltypes():    
    llama_2_70b = LLMModelType("Llama-2-70b", "meta/llama-2-70b-chat")
    llama_2_13b = LLMModelType("Llama-2-13b", "meta/llama-2-13b-chat")
    llama_2_7b = LLMModelType("Llama-2-7b", "meta/llama-2-7b-chat")

    llama_3_70b = LLMModelType("Llama-3-70b", "meta/llama-3-70b-chat")
    llama_3_8b = LLMModelType("Llama-3-8b", "meta/llama-3-8b-chat")

    mistral_7b = LLMModelType("Mistral-7b", "mistralai/mistral-7b-instruct-v0.2")
    mistral_8x7b = LLMModelType("Mistral-8x7b", "mistralai/mixtral-8x7b-instruct-v0.1")

    return [llama_2_70b, llama_2_13b, llama_2_7b, llama_3_70b, llama_3_8b, mistral_7b, mistral_8x7b]



