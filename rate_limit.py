from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

DEFAULT_LIMITER = "1/second"
SMALL_LIMITER = "2/second"
LARGE_LIMITER = "1 per 2 seconds; 10 per minute;"