FROM python:3.10

RUN apt-get update -y
RUN apt-get upgrade -y

COPY app.py app.py
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

ENTRYPOINT streamlit run app.py