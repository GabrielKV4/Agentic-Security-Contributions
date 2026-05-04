import asyncio
from typing import Callable, Any
from .rate_limiter import TokenBucketRateLimiter

def estimate_tokens(*args, **kwargs) -> int:
    text = " ".join(str(a) for a in args) + " " + " ".join(str(v) for v in kwargs.values())
    return int(len(text) * 0.25)
class RateLimitedExecutor:
    
    def __init__(self, 
                 rpm_limiter: TokenBucketRateLimiter,
                 tpm_limiter: TokenBucketRateLimiter, 
                 max_retries: int = 3,
                 estimated_tokens: int = 300):
        self.rpm_limiter = rpm_limiter
        self.tpm_limiter = tpm_limiter
        self.max_retries = max_retries
        self.estimated_tokens = estimated_tokens
        self._lock = asyncio.Lock()
    
    async def execute(self, func: Callable, *args, **kwargs) -> Any:
        
        retries = 0
        
        while True:
            estimated_tokens = self.estimated_tokens
            
            
            await self.rpm_limiter.acquire(1)
            await self.tpm_limiter.acquire(estimated_tokens)
            
            try:
                return await func(*args, **kwargs)
            
            except Exception as e:
                
                if retries < self.max_retries:
                    retries += 1
                    wait_time = min(2 ** retries, 5)
                    
                    if "rate limit" in str(e).lower():
                        wait_time += 1
                    
                    await asyncio.sleep(wait_time)
                    continue
                raise e