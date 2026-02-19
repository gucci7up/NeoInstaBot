import time
from collections import defaultdict
from app.config import Config

# Simple in-memory rate limiter using fixed window
class RateLimiter:
    def __init__(self, limit: int = 5, window: int = 60):
        self.limit = limit
        self.window = window
        self.requests = defaultdict(list)

    def is_allowed(self, user_id: int) -> bool:
        now = time.time()
        # Clean up old requests
        self.requests[user_id] = [t for t in self.requests[user_id] if now - t < self.window]
        
        if len(self.requests[user_id]) < self.limit:
            self.requests[user_id].append(now)
            return True
        return False

rate_limiter = RateLimiter(limit=5, window=60)

def is_admin(user_id: int) -> bool:
    return user_id == Config.ADMIN_TELEGRAM_ID
