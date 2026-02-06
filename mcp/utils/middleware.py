"""Middleware utilities for MCP Server"""

import time
import logging
from functools import wraps
from typing import Callable, Any
from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
import jwt
from datetime import datetime
from config import config


# Set up logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def authenticate_request(request: Request) -> dict:
    """
    Authenticate incoming request using JWT token
    """
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = auth_header.split(" ")[1]

    try:
        # Decode the JWT token
        payload = jwt.decode(token, config.api_key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def log_request_middleware(func: Callable) -> Callable:
    """
    Middleware decorator to log incoming requests
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs.get('request') or (args[0] if args else None)

        if request:
            start_time = time.time()
            client_ip = request.client.host if request.client else "unknown"

            logger.info(f"Request received: {request.method} {request.url.path} from {client_ip}")

            try:
                result = await func(*args, **kwargs)

                # Calculate processing time
                duration = time.time() - start_time

                logger.info(f"Request completed: {request.method} {request.url.path} "
                           f"Status: 200, Duration: {duration:.3f}s")

                return result
            except Exception as e:
                duration = time.time() - start_time
                logger.error(f"Request failed: {request.method} {request.url.path} "
                            f"Status: 500, Duration: {duration:.3f}s, Error: {str(e)}")
                raise
        else:
            # If no request object, just call the function
            return await func(*args, **kwargs)

    return wrapper


def authentication_middleware(func: Callable) -> Callable:
    """
    Middleware decorator to authenticate requests
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs.get('request') or (args[0] if args else None)

        if request:
            # Authenticate the request
            user_payload = authenticate_request(request)
            # Add user info to kwargs for use in the function
            kwargs['user_info'] = user_payload

        return await func(*args, **kwargs)

    return wrapper


class LoggingMiddleware:
    """
    ASGI Middleware for logging requests
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        start_time = time.time()

        # Send response and capture status
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                status_code = message["status"]
                duration = time.time() - start_time

                request_method = scope.get("method", "UNKNOWN")
                request_path = scope.get("path", "UNKNOWN")

                logger.info(f"Request: {request_method} {request_path} "
                           f"Status: {status_code}, Duration: {duration:.3f}s")

            await send(message)

        await self.app(scope, receive, send_wrapper)


class AuthenticationMiddleware:
    """
    ASGI Middleware for authenticating requests
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or "headers" not in scope:
            return await self.app(scope, receive, send)

        # Allow health checks and root without authentication
        path = scope.get("path", "")
        if path in ["/", "/health", "/ready"]:
            return await self.app(scope, receive, send)

        # Extract headers
        headers = {k.decode().lower(): v.decode() for k, v in scope["headers"]}

        auth_header = headers.get("authorization")

        if not auth_header or not auth_header.startswith("bearer "):
            # Send 401 Unauthorized response
            response = JSONResponse(
                status_code=401,
                content={"detail": "Missing or invalid Authorization header"}
            )
            await response(scope, receive, send)
            return

        token = auth_header.split(" ", 1)[1]

        try:
            # Decode the JWT token
            payload = jwt.decode(token, config.api_key, algorithms=["HS256"])
            # Add user info to scope for downstream handlers
            scope["user_info"] = payload
        except jwt.ExpiredSignatureError:
            response = JSONResponse(
                status_code=401,
                content={"detail": "Token has expired"}
            )
            await response(scope, receive, send)
            return
        except jwt.InvalidTokenError:
            response = JSONResponse(
                status_code=401,
                content={"detail": "Invalid token"}
            )
            await response(scope, receive, send)
            return

        await self.app(scope, receive, send)