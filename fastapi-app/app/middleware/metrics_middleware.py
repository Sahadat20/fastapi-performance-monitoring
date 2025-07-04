
# Middleware for tracking HTTP request metrics
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
from app.metrics.metrics import http_requests_total, http_request_duration
class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time

        route = request.url.path
        method = request.method
        status_code = response.status_code

        http_requests_total.labels(method=method, route=route, status_code=status_code).inc()
        http_request_duration.labels(method=method, route=route, status_code=status_code).observe(duration)

        return response