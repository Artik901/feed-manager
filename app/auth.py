from flask_login import UserMixin
from app.settings_manager import load_settings


class User(UserMixin):

    def __init__(self, username):
        self.id = username


def check_login(username, password):

    settings = load_settings()

    auth = settings.get(
        "auth",
        {}
    )

    return (
        username == auth.get("username")
        and
        password == auth.get("password")
    )