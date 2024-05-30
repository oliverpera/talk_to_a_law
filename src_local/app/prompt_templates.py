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

template_role = """
    Als Professor für Bankrecht bist du speziell darauf ausgerichtet, komplexe rechtliche Fragen mit hoher Genauigkeit und Fachkenntnis zu beantworten. Deine Aufgabe besteht darin, präzise und juristisch korrekte Informationen zu liefern, basierend auf den bereitgestellten Details.
    
    ---
    {query}
    ---

    Verwende den nachfolgenden Kontext, um deine Antwort zu informieren und zu veranschaulichen:
    ---
    {context}
    ---

    Deine Antwort sollte in Form eines detaillierten Fließtexts vorliegen, der ausschließlich auf die gestellte Frage bezogen ist. Achte darauf, dass deine Antwort nicht durch unnötige Kommentare oder zusätzliche Informationen beeinträchtigt wird. Ziel ist es, eine klare, prägnante und direkt auf die Frage zugeschnittene Antwort zu liefern.     
    """

prompt_template_role_prompting = PromptTemplate(
        input_variables=["query", "context"],
        template=template_role,
)


####################################################################################################
# Prompt templates for zero shot
####################################################################################################


template_zero_shot = """
   Beantworte folgende Frage im Zusammenhang mit dem deutschen Bankrecht. Es ist wichtig, dass deine Antwort sowohl präzise als auch fachlich korrekt formuliert ist.
    ---
    {query}
    ---

    Berücksichtige für die Beantwortung der Frage folgenden Kontextinformation:
    ---
    {context}
    ---

    Stelle sicher, dass deine Antwort ausschließlich in Form eines detaillierten Fließtexts vorliegt. Vermeide jegliche zusätzlichen Bemerkungen oder Erläuterungen, die nicht direkt zur Beantwortung der gestellten Frage beitragen.
    """

prompt_template_zero_shot = PromptTemplate(
        input_variables=["query", "context"],
        template=template_zero_shot,
)


####################################################################################################
# Prompt templates for one shot
####################################################################################################

template_one_shot = """
    TEST 
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
        template=template_one_shot,
)

############# Baseline Template ####################
template_baseline_role = """
    Als Professor für Bankrecht bist du speziell darauf ausgerichtet, komplexe rechtliche Fragen mit hoher Genauigkeit und Fachkenntnis zu beantworten. Deine Aufgabe besteht darin, präzise und juristisch korrekte Informationen zu liefern, basierend auf den bereitgestellten Details.
    
    ---
    {query}
    ---

    Deine Antwort sollte in Form eines detaillierten Fließtexts vorliegen, der ausschließlich auf die gestellte Frage bezogen ist. Achte darauf, dass deine Antwort nicht durch unnötige Kommentare oder zusätzliche Informationen beeinträchtigt wird. Ziel ist es, eine klare, prägnante und direkt auf die Frage zugeschnittene Antwort zu liefern.     
    """

prompt_template_baseline_role_prompting = PromptTemplate(
        input_variables=["query"],
        template=template_baseline_role,
)

template_baseline_zero_shot = """
   Beantworte folgende Frage im Zusammenhang mit dem deutschen Bankrecht. Es ist wichtig, dass deine Antwort sowohl präzise als auch fachlich korrekt formuliert ist.
    
    ---
    {query}
    ---

    Stelle sicher, dass deine Antwort ausschließlich in Form eines detaillierten Fließtexts vorliegt. Vermeide jegliche zusätzlichen Bemerkungen oder Erläuterungen, die nicht direkt zur Beantwortung der gestellten Frage beitragen.
    """

prompt_template_baseline_zero_shot = PromptTemplate(
        input_variables=["query"],
        template=template_baseline_zero_shot,
)

