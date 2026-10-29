# FrontierSWE Task: Distributed Rate Limiter Race Condition

> **Thesis:** Evaluating an AI agent on a single-threaded algorithm is insufficient. To test true software engineering capability, the agent must reason about distributed state, concurrency, and atomicity. This is a Principal-level FrontierSWE benchmark task.

## The Problem
The agent is presented with a FastAPI application backed by Redis. The API has a rate limiter that works perfectly under sequential load but fails catastrophically under concurrent load. 

Because the rate-limiting logic uses a naive `GET` then `SET` pattern, a race condition occurs. If 20 requests hit the endpoint at the exact same millisecond, the counter fails to update atomically, and all 20 requests bypass the limit of 5.

## The Agent's Mission
1. Analyze the FastAPI codebase (`src/app.py`).
2. Identify the race condition in the Redis logic.
3. Implement a fix using strict atomicity (Redis `INCR` or a Lua script). *Note: A Python threading lock is not sufficient for a distributed environment.*
4. Ensure the hidden test suite passes, which validates both concurrency limits and time-window resets.

## The Validation (Proof of Work)
I rigorously validated this task to ensure it meets the FrontierSWE standard:

*   **Vulnerability Verified:** I proved the bug exists. Firing 20 concurrent threads resulted in `20 successes` (when the limit is 5).
*   **Oracle Verified:** The reference solution (`solution/solve.sh`) patches the code using Redis `INCR`. Re-running the test results in exactly `5 successes` and `15 failures` (`1 passed`).
*   **Time-Window Verified:** The test suite also validates that the rate limit correctly resets after the 60-second window expires.

## Folder Structure
This task strictly follows the Harbor/FrontierSWE v2 scaffold:

    .
    ├── instruction.md       # The prompt provided to the agent
    ├── task.toml            # Task configuration (max agent time, etc.)
    ├── Dockerfile           # Isolated environment with Redis and Pytest
    ├── src/
    │   └── app.py           # The vulnerable FastAPI application
    ├── tests/
    │   └── test_concurrency.py  # Hidden verifier (fails on buggy code, passes on fix)
    └── solution/
        └── solve.sh         # The reference solution (uses Redis INCR)

## How to Run (Local Verification)

1. Build the Docker image:

    docker build -t rate-limiter-task .

2. To verify the vulnerability, run the tests against the buggy code (this should FAIL):

    docker run rate-limiter-task pytest tests/

3. To verify the solution, run the reference script then run the tests again (this should PASS):

    docker run rate-limiter-task bash -c "bash solution/solve.sh && pytest tests/"

## Author
**Anuoluwapo Daniel Ojo**
Senior Data Analyst | Data & AI Engineer
[GitHub](https://github.com/Daniel38215571) | [LinkedIn](https://linkedin.com/in/daniel-ojo-879273197)
