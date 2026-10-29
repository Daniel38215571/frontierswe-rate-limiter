#!/bin/bash

cat << 'EOF' > src/app.py
from fastapi import FastAPI, HTTPException
from redis import Redis
import time
import os

app = FastAPI()

redis_client = Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))

RATE_LIMIT = 5
WINDOW_SIZE = 60

@app.get("/api/data")
def get_data(user_id: str):
    key = f"ratelimit:{user_id}:{int(time.time() // WINDOW_SIZE)}"
    
    # THE FIX: Use INCR for atomicity
    current_count = redis_client.incr(key)
    
    if current_count == 1:
        redis_client.expire(key, WINDOW_SIZE)
        
    if current_count > RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Too Many Requests")
        
    return {"status": "ok", "message": "You have accessed the data"}
EOF
