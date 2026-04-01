from app.data.repository import InMemoryRepository


class AuthService:
    def __init__(self, repo: InMemoryRepository | None = None) -> None:
        self.repo = repo or InMemoryRepository.get_instance()

    def authenticate(self, username: str, password: str) -> bool:
        user = self.repo.get_user_by_username(username)
        if not user:
            return False
        return user["password"] == password
