FROM python:3.8-alpine

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

COPY . .

RUN pip install -r requirements.txt
