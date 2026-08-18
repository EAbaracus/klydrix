import asyncio
import time


class RateLimiter:
    """Token bucket rate limiter.

    Args:
        calls_per_minute: Maximum number of calls allowed per minute.
    """

    def __init__(self, calls_per_minute: int):
        if calls_per_minute < 0:
            raise ValueError("calls_per_minute must be non-negative")
        self.calls_per_minute = calls_per_minute
        self.refill_rate = calls_per_minute / 60.0  # tokens per second
        self.tokens = float(calls_per_minute)  # start with a full bucket
        self.last_refill = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        """Wait until a token is available."""
        if self.calls_per_minute == 0:
            # Never allow a call
            await asyncio.sleep(float("inf"))
            return

        while True:
            async with self._lock:
                now = time.monotonic()
                elapsed = now - self.last_refill
                # Refill tokens based on elapsed time
                self.tokens = min(
                    self.calls_per_minute,
                    self.tokens + elapsed * self.refill_rate,
                )
                self.last_refill = now

                if self.tokens >= 1.0:
                    self.tokens -= 1.0
                    return

                # Not enough tokens, compute wait time for one token
                wait_time = (1.0 - self.tokens) / self.refill_rate

            # Wait outside the lock to allow other coroutines to proceed
            await asyncio.sleep(wait_time)
