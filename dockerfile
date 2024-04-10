FROM python:3.11

RUN pip install --upgrade pip
RUN mkdir -p /app/emailclassifier

WORKDIR /app/talktoalaw

COPY requirements.txt /app/talktoalaw

RUN pip install -r requirements.txt

# do not change the arguments
ENTRYPOINT ["chainlit", "run", "app.py", "--host=0.0.0.0", "--port=80", "--headless"]


