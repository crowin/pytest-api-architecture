from core.api.auth_client import get_user_session


class User:
    def __init__(self, user_id: int, username: str, password: str):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.token = get_user_session(self.username)