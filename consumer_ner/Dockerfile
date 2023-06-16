FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download de_core_news_sm
RUN python -m spacy download es_core_news_sm
RUN python -m spacy download uk_core_news_sm

COPY src src