from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from datetime import datetime, timedelta
from collections import defaultdict

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, rate_limit: int = 2, time_window: int = 60):
        super().__init__(app)
        self.rate_limit = rate_limit  # Max number of requests
        self.time_window = time_window  # Time window in seconds (60 seconds = 1 minute)
        self.requests = defaultdict(list)  # Store user requests with timestamp


    async def dispatch(self, request: Request, call_next):
        # Get the client's IP address
        client_ip = request.client.host
        print(f"Client IP: {client_ip}")
        print("hit")
        # Get the current time
        current_time = datetime.now()

        # Check if the IP address is already in the request dictionary
        if client_ip in self.requests:
            # Clean up any old requests (outside the time window)
            self.requests[client_ip] = [t for t in self.requests[client_ip] if current_time - t < timedelta(seconds=self.time_window)]

            # If request count exceeds limit, return 429 Too Many Requests
            if len(self.requests[client_ip]) >= self.rate_limit:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Too many requests. Please try again later."}
                )

        else:
            # Initialize the request history for the IP address
            self.requests[client_ip] = []

        # Add the current request timestamp to the list of requests
        self.requests[client_ip].append(current_time)

        # Proceed with the request if within limits
        response = await call_next(request)
        return response

"""
For testing middlewares: 
curl -v -X POST -H "x-api-key: env_key" "localhost:8000/execute"
"""