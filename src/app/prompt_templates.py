from langchain.prompts import PromptTemplate

####################################################################################################
# Prompt templates for the different chains
# Base template
####################################################################################################

template = """
    Beantworte folgende Frage in deutscher Sprache:
    ---
    {query}
    ---

    Nutze hierfür folgenden Kontext:
    ---
    {context}
    ---
    """

prompt_template = PromptTemplate(
        input_variables=["query", "context"],
        template=template,
)


####################################################################################################
# Prompt templates for role prompting
####################################################################################################

template_role_prompting = """
    Beantworte folgende Frage in deutscher Sprache:
    ---
    {query}
    ---

    Nutze hierfür folgenden Kontext:
    ---
    {context}
    ---
    """

prompt_template_role_prompting = PromptTemplate(
        input_variables=["query", "context"],
        template=template,
)


####################################################################################################
# Prompt templates for zero shot
####################################################################################################

template_zero_shot = """
    Beantworte folgende Frage in deutscher Sprache:
    ---
    {query}
    ---

    Nutze hierfür folgenden Kontext:
    ---
    {context}
    ---
    """

prompt_template_zero_shot = PromptTemplate(
        input_variables=["query", "context"],
        template=template,
)


####################################################################################################
# Prompt templates for one shot
####################################################################################################

template_one_shot = """
    Beantworte folgende Frage in deutscher Sprache:
    ---
    {query}
    ---

    Nutze hierfür folgenden Kontext:
    ---
    {context}
    ---
    """

prompt_template_one_shot = PromptTemplate(
        input_variables=["query", "context"],
        template=template,
)
