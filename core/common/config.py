import os

class Config:
    BASE_URL = os.getenv("BASE_URL")
    MARKET_API_URL = f"{BASE_URL}/{os.getenv('MARKET_API')}"
    USERS_API_URL = f"{BASE_URL}/{os.getenv('USERS_API')}"
    USER_SESSIONS_DIR = os.getenv('USER_SESSIONS_DIR')