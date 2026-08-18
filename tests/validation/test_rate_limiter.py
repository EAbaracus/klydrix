import asyncio
import time
import pytest
from launch_engine.validation.rate_limiter import RateLimiter


@pytest.mark.asyncio
async def test_burst():
    """Test that rate limiter allows burst up to calls_per_minute."""
    calls_per_minute = 5
    limiter = RateLimiter(calls_per_minute)

    # Should be able to make `calls_per_minute` calls immediately
    start = time.monotonic()
    tasks = [limiter.acquire() for _ in range(calls_per_minute)]
    await asyncio.gather(*tasks)
    elapsed = time.monotonic() - start

    # Burst should be instantaneous (or very fast)
    assert elapsed < 0.1  # Allow a small margin for scheduling

    # Next call should be blocked
    start = time.monotonic()
    await limiter.acquire()
    elapsed = time.monotonic() - start

    # Should have waited at least enough time to earn one token
    # One token every 60/calls_per_minute seconds
    min_wait = 60.0 / calls_per_minute
    assert elapsed >= min_wait * 0.9  # Allow 10% tolerance for timing inaccuracies


@pytest.mark.asyncio
async def test_rate_limit_over_time():
    """Test that rate limiter enforces rate limit over time."""
    calls_per_minute = 10  # 1 per 6 seconds
    limiter = RateLimiter(calls_per_minute)
    num_calls = 20  # burst of 10, then 10 more

    start = time.monotonic()
    for _ in range(num_calls):
        await limiter.acquire()
    elapsed = time.monotonic() - start

    # Expected minimum time: burst of calls_per_minute calls (immediate)
    # then the remaining calls at the refill rate.
    if num_calls <= calls_per_minute:
        expected_min = 0.0
    else:
        expected_min = (num_calls - calls_per_minute) * (60.0 / calls_per_minute)
    # We expect the elapsed time to be at least expected_min (since the burst is free)
    # and at most expected_min plus the time for one burst (which is negligible)
    # plus some slack.
    # Allow 20% tolerance for scheduling inaccuracies.
    assert (
        elapsed >= expected_min * 0.8
    ), f"Expected at least {expected_min * 0.8}s, got {elapsed}s"
    assert (
        elapsed <= expected_min * 1.2
    ), f"Expected at most {expected_min * 1.2}s, got {elapsed}s"


@pytest.mark.asyncio
async def test_concurrent_access():
    """Test concurrent access from multiple coroutines."""
    calls_per_minute = 10  # Burst of 10
    limiter = RateLimiter(calls_per_minute)

    # Start 20 concurrent acquire tasks
    tasks = [asyncio.create_task(limiter.acquire()) for _ in range(20)]
    # Wait for 0.5 seconds (less than the time to earn one token: 6 seconds)
    done, pending = await asyncio.wait(tasks, timeout=0.5)
    # Cancel pending tasks
    for task in pending:
        task.cancel()
    # Wait for cancellation to complete
    if pending:
        await asyncio.gather(*pending, return_exceptions=True)
    # Exactly the burst size should have completed
    assert (
        len(done) == calls_per_minute
    ), f"Expected {calls_per_minute} done tasks, got {len(done)}"


@pytest.mark.asyncio
async def test_zero_calls_per_minute():
    """Test that rate limiter handles zero calls_per_minute gracefully."""
    limiter = RateLimiter(0)

    # This should not return (or take a very long time)
    # We'll test by trying to wait for a short time and expecting it to not complete
    try:
        # Wait for 0.5 seconds, but the acquire should not complete
        await asyncio.wait_for(limiter.acquire(), timeout=0.5)
        # If we get here, it returned too soon
        assert False, "acquire() returned too soon for zero calls_per_minute"
    except asyncio.TimeoutError:
        # This is expected
        pass  # We don't check the exact elapsed time to avoid flakiness


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
