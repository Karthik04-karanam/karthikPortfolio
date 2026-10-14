"""
FastAPI Dependencies & Abuse Prevention
Includes client IP detection, sliding window rate limiting, and request validation helpers.
"""
import time
from collections import defaultdict
from typing import Dict, List
from fastapi import Request, HTTPException, status
from app.config import settings


class InMemoryRateLimiter:
    """
    Sliding window in-memory rate limiter per client IP address.
    Thread-safe for standard single-process Uvicorn workers and test suites.
    """

    def __init__(self, max_requests: int = 5, window_seconds: int = 600):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._ip_history: Dict[str, List[float]] = defaultdict(list)

    def check(self, ip: str) -> None:
        """
        Check if the IP has exceeded allowed requests in the time window.
        Raises HTTPException(429) if exceeded.
        """
        now = time.time()
        window_start = now - self.window_seconds

        # Filter out timestamps older than the sliding window
        valid_timestamps = [t for t in self._ip_history[ip] if t > window_start]
        self._ip_history[ip] = valid_timestamps

        if len(valid_timestamps) >= self.max_requests:
            retry_after = int(valid_timestamps[0] + self.window_seconds - now) + 1
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Too many requests from this address. Please wait {max(1, retry_after)} seconds before trying again.",
                headers={"Retry-After": str(max(1, retry_after))}
            )

        # Record this request timestamp
        self._ip_history[ip].append(now)

    def reset(self) -> None:
        """Reset all rate limiter state. Useful for test suites."""
        self._ip_history.clear()


# Global rate limiter instance
rate_limiter = InMemoryRateLimiter(
    max_requests=settings.RATE_LIMIT_MAX_REQUESTS,
    window_seconds=settings.RATE_LIMIT_WINDOW_SECONDS
)


def get_client_ip(request: Request) -> str:
    """
    Extract client IP address safely from Request.
    Inspects X-Forwarded-For header when behind reverse proxies, falling back to client.host.
    """
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        # First IP in chain is client IP
        return forwarded.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "127.0.0.1"


async def check_contact_rate_limit(request: Request) -> None:
    """FastAPI dependency to rate limit contact form submissions."""
    ip = get_client_ip(request)
    rate_limiter.check(ip)
