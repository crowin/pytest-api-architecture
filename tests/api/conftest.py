import json
import shutil
from pathlib import Path

import pytest

from core.api.user.auth_client import auth_user
from core.api.market.market_client import MarketApi
from core.common.user import User
from core.common.config import Config
from tests.test_user import TestUser


def pytest_configure(config):
    print("Preparing config")
    _init_all_sessions()


def pytest_sessionfinish(session, exitstatus):
    if not hasattr(session.config, "workerinput"):
        print("Tear down config")
        _remove_all_sessions()

@pytest.fixture(scope="session")
def basic_user():
    yield TestUser.FIRST_USER

@pytest.fixture(scope="session")
def basic_user_api(basic_user):
    yield MarketApi(basic_user)


def _init_all_sessions():
    project_root = Path().resolve()
    folder = project_root / Config.USER_SESSIONS_DIR
    if not folder.exists():
        folder.mkdir()
    for key, user in TestUser.__dict__.items():
        if not isinstance(user, User):
            continue
        user_file = folder / f"{user.username}_token.json"
        if not user_file.exists():
            resp = auth_user(user.username, user.password)
            resp.raise_for_status()
            token = resp.json()["token"]
            with user_file.open("w", encoding="utf-8") as f:
                json.dump(token, f, ensure_ascii=False, indent=4)
            print(f"Session file created for {user.username}")

def _remove_all_sessions():
    project_root = Path().resolve()
    folder = project_root / Config.USER_SESSIONS_DIR
    if folder.exists():
        print("Session files removed")
        shutil.rmtree(folder)