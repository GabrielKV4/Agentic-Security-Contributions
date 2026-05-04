"""Advanced concurrent execution package for security scanning."""

from agentic_security.config import settings_var
from agentic_security.executor.rate_limited_executor import RateLimitedExecutor
from agentic_security.executor.rate_limiter import TokenBucketRateLimiter
from agentic_security.executor.circuit_breaker import CircuitBreaker
from agentic_security.executor.concurrent import ConcurrentExecutor, ExecutorMetrics

from agentic_security.executor.rate_limiter import TokenBucketRateLimiter, TPMSlidingWindowLimiter

rpm = settings_var("rate_limit.rpm", 30)
tpm = settings_var("rate_limit.tpm", 6000)

estimated_tokens = settings_var("rate_limit.estimated_tokens_per_request", 300)

rpm_limiter = TokenBucketRateLimiter(
    rate=rpm / 60,
    burst=rpm
)

tpm_limiter = TokenBucketRateLimiter(
    rate=tpm / 60,
    burst=tpm
)

executor = RateLimitedExecutor(
    rpm_limiter=rpm_limiter,
    tpm_limiter=tpm_limiter,
    estimated_tokens=estimated_tokens
)


__all__ = [
    "TokenBucketRateLimiter",
    "CircuitBreaker",
    "ConcurrentExecutor",
    "ExecutorMetrics",
    "executor",
]
