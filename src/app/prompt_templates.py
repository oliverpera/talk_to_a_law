from langchain.prompts import PromptTemplate

template = """
    Beantworte folgende Frage:
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
