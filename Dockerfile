FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y redis-server
RUN pip install fastapi uvicorn redis pytest httpx

COPY . .

CMD service redis-server start && pytest tests/
