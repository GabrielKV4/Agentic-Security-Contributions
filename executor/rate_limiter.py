"""Token bucket rate limiter for controlling request rate."""

import asyncio
from collections import deque
import time

class TPMSlidingWindowLimiter:
    """ """
    def __init__(self, tpm: int):
        self.tpm = tpm
        self.events = deque()
        self.used = 0
        self._lock = asyncio.Lock()

    def _cleanup(self):
        now = time.monotonic()
        while self.events and now - self.events[0][0] > 60:
            _, tokens = self.events.popleft()
            self.used -= tokens

    async def acquire(self, tokens: int):
        async with self._lock:
            while True:
                self._cleanup()

                if self.used + tokens <= self.tpm:
                    self.events.append((time.monotonic(), tokens))
                    self.used += tokens
                    return

                wait_time = 60 - (time.monotonic() - self.events[0][0])
                await asyncio.sleep(max(wait_time, 0.05))

class TokenBucketRateLimiter:
    """Token bucket rate limiter with configurable rate and burst capacity.

    This implements the token bucket algorithm where tokens are added at a fixed
    rate and consumed for each request. Supports bursting up to the bucket capacity.

    Example:
        >>> limiter = TokenBucketRateLimiter(rate=10, burst=20)
        >>> await limiter.acquire()  # Will wait if no tokens available
    """

    def __init__(self, rate: float, burst: int):
        """Initialize rate limiter.

        Args:
            rate: Tokens added per second (requests/sec)
            burst: Maximum bucket capacity (max concurrent burst)
        """
        self.rate = rate
        self.burst = burst
        self.tokens = float(burst)
        self.last_update = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self, tokens: float = 1):
        """Acquire a token, waiting if necessary.

        This method will block until a token is available.
        """
        async with self._lock:
            while True:
                now = time.monotonic()
                elapsed = now - self.last_update
                
                self.tokens = min(self.burst, self.tokens + elapsed * self.rate)
                self.last_update = now
                
                if self.tokens >= tokens:
                    self.tokens -= tokens
                    return
                
                needed = tokens - self.tokens
                wait_time = needed / self.rate
                
                await asyncio.sleep(wait_time)

    def get_available_tokens(self) -> float:
        """Get current number of available tokens (non-blocking).

        Returns:
            float: Number of tokens currently available
        """
        now = time.monotonic()
        elapsed = now - self.last_update
        return min(self.burst, self.tokens + elapsed * self.rate)
