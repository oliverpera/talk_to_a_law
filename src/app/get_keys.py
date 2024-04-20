import os
from dotenv import load_dotenv

# Lade die Umgebungsvariablen aus der .env-Datei
load_dotenv()

api_key = os.getenv("HELLSTERN_API_KEY")
print(api_key)