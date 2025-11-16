import time

REQUEST_COUNTS = {}
RATE_LIMIT = 100
WINDOW_SECONDS = 3600

def is_allowed(client_id: str) -> bool:
    now = int(time.time())
    window_start = now - WINDOW_SECONDS

    if client_id not in REQUEST_COUNTS:
        REQUEST_COUNTS[client_id] = []

    REQUEST_COUNTS[client_id] = [
        t for t in REQUEST_COUNTS[client_id] if t >= window_start
    ]

    if len(REQUEST_COUNTS[client_id]) >= RATE_LIMIT:
        return False

    REQUEST_COUNTS[client_id].append(now)
    return True
