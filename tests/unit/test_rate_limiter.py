from src.rate_limiter import is_allowed, REQUEST_COUNTS

def test_first_request_is_allowed():
    REQUEST_COUNTS.clear()
    assert is_allowed("user1") is True


def test_rate_limit_exceeded():
    REQUEST_COUNTS.clear()
    for _ in range(100):
        is_allowed("user2")
    assert is_allowed("user2") is False
