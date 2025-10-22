import os

from core.common.user import User


def _build_user(username: str):
    return User(int(os.getenv(f"{username}_USER_ID")), os.getenv(f"{username}_USER_NAME"), os.getenv(f"{username}_USER_PASSWORD"))


class TestUser:
    BASIC_USER: User = _build_user("BASIC")
    SECOND_USER: User = _build_user("SECOND")