import json
from pathlib import Path

import allure
import requests
from requests import Response

from core.common.config import Config

@allure.step("Auth {username} user")
def auth_user(username, password) -> Response:
    return requests.post(f"{Config.USERS_API_URL}/login", json={"username": username, "password": password})


@allure.step("Get user {username} session")
def get_user_session(username):
    project_root = Path().resolve()
    folder = project_root / Config.USER_SESSIONS_DIR
    user_file = folder / f"{username}_token.json"
    if not user_file.exists():
        return None
    with user_file.open("r", encoding="utf-8") as f:
        return json.load(f)