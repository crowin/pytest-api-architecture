import os

class Config:
    BASE_URL = os.getenv("BASE_URL")
    CARTS_API_URL = f"{BASE_URL}/{os.getenv('CARTS_API')}"
    AUTH_API_URL = f"{BASE_URL}/{os.getenv('AUTH_API')}"
    USER_SESSIONS_DIR = os.getenv('USER_SESSIONS_DIR')
