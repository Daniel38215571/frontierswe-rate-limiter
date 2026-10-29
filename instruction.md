# Fix the Race Condition in the Distributed Rate Limiter

You are a Principal Engineer working on a high-traffic financial API. 
The API uses Redis to rate-limit requests. 

## The Bug
Under concurrent load, the rate limiter is failing. If 10 requests hit the API at the exact same millisecond, all 10 are allowed through, even if the limit is 5. 

## Your Task
1. Analyze `src/app.py`.
2. Identify the race condition in how the rate limit counter is incremented in Redis.
3. Fix the logic to ensure atomicity (e.g., using Redis pipelines, `INCR`, or Lua scripts).
4. Ensure the tests in `tests/` pass.
