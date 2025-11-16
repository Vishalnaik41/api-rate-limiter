from fastapi import FastAPI, Request, HTTPException
import time

app = FastAPI()

REQUEST_COUNTS = {}
RATE_LIMIT = 100  # requests per hour
WINDOW_SECONDS = 3600


def is_allowed(client_id: str) -> bool:
    now = int(time.time())
    window_start = now - WINDOW_SECONDS

    if client_id not in REQUEST_COUNTS:
        REQUEST_COUNTS[client_id] = []

    # keep only recent timestamps
    REQUEST_COUNTS[client_id] = [
        t for t in REQUEST_COUNTS[client_id] if t >= window_start
    ]

    if len(REQUEST_COUNTS[client_id]) >= RATE_LIMIT:
        return False

    REQUEST_COUNTS[client_id].append(now)
    return True


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_id = request.headers.get("X-API-Key", "anonymous")

    if not is_allowed(client_id):
        raise HTTPException(
            status_code=429,
            detail={"error": "Rate limit exceeded", "retry_after": 60},
        )

    response = await call_next(request)
    return response


@app.get("/api/data")
async def get_data():
    return {"message": "Here is your data"}
