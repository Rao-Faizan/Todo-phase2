from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from fastapi import FastAPI

# Create limiter instance with 100 requests per minute
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

def setup_rate_limiter(app: FastAPI):
    """Setup rate limiter for the application"""
    app.state.limiter = limiter
    app.add_exception_handler(429, _rate_limit_exceeded_handler)

    # Apply rate limiting to all routes, excluding built-in OpenAPI routes
    for route in app.routes:
        # Skip built-in OpenAPI routes that don't have request/websocket parameters
        # These include docs, redoc, openapi.json, and internal redirect routes
        if hasattr(route, 'path'):
            if route.path in ["/docs", "/redoc", "/openapi.json"]:
                continue

        # Also skip internal routes by checking if the endpoint function name contains certain keywords
        if hasattr(route, 'endpoint') and route.endpoint.__name__ in ['swagger_ui_redirect', 'openapi']:
            continue

        # Skip rate limiting for OPTIONS requests (needed for CORS preflight)
        if hasattr(route, 'methods') and 'OPTIONS' in route.methods:
            continue
        # Apply rate limiting to all other methods
        elif hasattr(route, 'methods') and 'GET' in route.methods:
            route.endpoint = limiter.limit("100/minute")(route.endpoint)
        elif hasattr(route, 'methods') and 'POST' in route.methods:
            route.endpoint = limiter.limit("100/minute")(route.endpoint)
        elif hasattr(route, 'methods') and 'PUT' in route.methods:
            route.endpoint = limiter.limit("100/minute")(route.endpoint)
        elif hasattr(route, 'methods') and 'DELETE' in route.methods:
            route.endpoint = limiter.limit("100/minute")(route.endpoint)
        elif hasattr(route, 'methods') and 'PATCH' in route.methods:
            route.endpoint = limiter.limit("100/minute")(route.endpoint)