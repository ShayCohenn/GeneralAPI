from functools import wraps
from fastapi import Request, HTTPException
from constants import r

def rate_limiter(max_requests_per_second: int, max_requests_per_day: int = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs['request']
            if request is None:
                raise HTTPException(
                    detail={"error": "Request object not found in arguments"},
                    status_code=500
                )

            client_ip = request.client.host

            # Rate limit per second
            redis_key_sec = f"rate_limit:{client_ip}:per_second:{func.__name__}"
            sec_res = r.get(redis_key_sec)
            if sec_res and int(sec_res.decode("utf-8")) >= max_requests_per_second:
                raise HTTPException(
                    detail={"error": "Too many requests per second"},
                    status_code=429
                )

            # Rate limit per day
            if max_requests_per_day is not None:
                redis_key_day = f"rate_limit:{client_ip}:per_day:{func.__name__}"
                day_res = r.get(redis_key_day)
                if day_res and int(day_res.decode("utf-8")) >= max_requests_per_day:
                    raise HTTPException(
                        detail={"error": "Too many requests per day"},
                        status_code=429
                    )
                
            try:
                # Increment the request count for per second rate limit
                r.incr(redis_key_sec)
                r.expire(redis_key_sec, 1)  # Expire in 1 second

                # Increment the request count for per day rate limit
                if max_requests_per_day is not None:
                    r.incr(redis_key_day)
                    r.expire(redis_key_day, 86400)  # Expire in 1 day (86400 seconds)

                # Call the original function with the provided arguments
                return await func(*args, **kwargs)
            except Exception as e:
                return HTTPException(
                    detail={"error": str(e)},
                    status_code=500
                )

        return wrapper

    return decorator
