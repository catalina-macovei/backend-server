from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

import os


class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        api_key = request.headers.get("x-api-key")

        expected_api_key = os.getenv("API_KEY")

        if api_key != expected_api_key:
            print("API Key mismatch or missing")
            return JSONResponse(
                status_code=401,
                content={"detail": "Unauthorized: Invalid API key"}
            )

        response = await call_next(request)
        return response
