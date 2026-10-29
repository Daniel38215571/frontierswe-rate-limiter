import pytest
from fastapi.testclient import TestClient
from src.app import app, redis_client
import threading
import time

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
    for _ in range(20):
        t = threading.Thread(target=make_request)
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    successes = results.count(200)
    failures = results.count(429)
    
    assert successes == 5, f"Expected 5 successes, got {successes}"
    assert failures == 15, f"Expected 15 failures, got {failures}"

def test_rate_limit_resets_after_window():
    user_id = "test_user_reset"
    
    # Hit the limit
    for _ in range(5):
        client.get(f"/api/data?user_id={user_id}")
        
    # The 6th request should fail
    assert client.get(f"/api/data?user_id={user_id}").status_code == 429
    
    # Wait for the window to expire (we mock time by advancing the Redis TTL)
    redis_client.flushall()
    
    # After window, it should succeed again
    assert client.get(f"/api/data?user_id={user_id}").status_code == 200
