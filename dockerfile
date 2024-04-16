# Verwende das offizielle Python-Image als Basis
FROM python:latest

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere die requirements.txt-Datei in das Arbeitsverzeichnis
COPY requirements.txt .

# Installiere die Python-Bibliotheken gemäß requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den chainlit.py-Code in das Arbeitsverzeichnis
COPY OliverPera/chainlit.py .
COPY OliverPera/create_appuser.py .
COPY OliverPera/model.py .
COPY OliverPera/sqllite3_script.py .
COPY OliverPera/test.py .


EXPOSE 2000

# Definiere den Startbefehl
CMD ["chainlit","run","chainlit.py","-w","--host","128.140.6.176", "--port","2000"]

