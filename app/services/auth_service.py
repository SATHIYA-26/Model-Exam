from data.repository import Repository


class AuthService:
    def __init__(self, repo: Repository | None = None) -> None:
        self.repo = repo or Repository.get_instance()

    def authenticate(self, username: str, password: str) -> bool:
        user = self.repo.get_user_by_username(username)
        if not user:
            return False
        # user is a SQLAlchemy User model, so use attribute access
        return user.password == password
