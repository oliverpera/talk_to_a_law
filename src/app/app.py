import replicate 


system_prompt = "Du bist ein hilfsbereiter, freundlicher und verständlicher Assistent. Du hast Zugriff auf eine Wissensdatenbank für das Deutsche Bankrecht und kannst Fragen beantworten."
prompt = "Was sind mögliche Bestandteile des harten Kernkapitals? Gib mir eine ausführlich Antwort und zeige die jeweiligen Gesetzesartikel"

iterator = replicate.run(
    "mistralai/mixtral-8x7b-instruct-v0.1",
    input={
        "prompt": prompt,
        "system_prompt": system_prompt,
        },
    )

answer = ""
    
for text in iterator:
    #print(text)
    answer += text
        
print(answer)