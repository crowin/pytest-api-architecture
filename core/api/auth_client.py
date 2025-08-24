import json
from pathlib import Path

import allure
import requests

from core.config import Config

@allure.step("Auth user")
def auth_user(username, password) -> str:
    body={"username": username, "password": password, "expiresInMins": 30}
    resp = requests.post(f"{Config.AUTH_API_URL}/login", json=body)
    resp.raise_for_status()
    return resp.json()["accessToken"]

@allure.step("Get user session")
def get_user_session(username):
    project_root = Path().resolve()
    folder = project_root / Config.USER_SESSIONS_DIR
    user_file = folder / f"{username}_token.json"
    if not user_file.exists():
        return None
    with user_file.open("r", encoding="utf-8") as f:
        return json.load(f)