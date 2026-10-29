FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y redis-server
RUN pip install fastapi uvicorn redis pytest httpx

COPY . .

# Start redis in the background
RUN echo "service redis-server start" > /start_redis.sh
RUN chmod +x /start_redis.sh

ENTRYPOINT ["/start_redis.sh"]
CMD ["pytest", "tests/"]
