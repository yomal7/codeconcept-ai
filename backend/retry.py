import time
from collections.abc import Callable
from typing import TypeVar

R = TypeVar("R")


def call_with_retry(
    fn: Callable[[], R],
    *,
    is_retryable: Callable[[Exception], bool],
    retries: int = 3,
    delay_seconds: float = 2.0,
) -> R:
    """Call fn(), retrying with linear backoff while is_retryable(exc) is True.

    Shared by GeminiClient and GeminiTTSClient so retry/backoff logic
    lives in exactly one place instead of being copy-pasted per client.
    """
    last_error: Exception | None = None

    for attempt in range(retries):
        try:
            return fn()
        except Exception as exc:
            last_error = exc
            if is_retryable(exc) and attempt < retries - 1:
                time.sleep(delay_seconds * (attempt + 1))
                continue
            break

    assert last_error is not None
    raise last_error