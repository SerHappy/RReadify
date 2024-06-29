import logging
import time
from collections.abc import Callable

from fastapi import Request, Response

logger = logging.getLogger(__name__)


async def request_duration(request: Request, call_next: Callable) -> Response:
    """Middleware to log the request duration."""
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start
    logger.info("%s %s %.2fs", request.method, request.url, duration)
    return response
