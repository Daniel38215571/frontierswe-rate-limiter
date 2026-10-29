import pytest
from fastapi.testclient import TestClient
from src.app import app, redis_client
import threading

client = TestClient(app)

def setup_function():
    redis_client.flushall()

def test_rate_limiter_under_concurrency():
    user_id = "test_user_concurrent"
    results = []
    
    def make_request():
        response = client.get(f"/api/data?user_id={user_id}")
        results.append(response.status_code)
        
    threads = []
    # Fire 20 requests at the exact same time
    for _ in range(20):
        t = threading.Thread(target=make_request)
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    # Count successes (200) and failures (429)
    successes = results.count(200)
    failures = results.count(429)
    
    # The limit is 5. We expect exactly 5 successes and 15 failures.
    assert successes == 5, f"Expected 5 successes, got {successes}"
    assert failures == 15, f"Expected 15 failures, got {failures}"
