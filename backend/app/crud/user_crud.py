from app.schemas.user import UserCreate, UserOut


class UserCRUD:
    _users: list[UserOut] = []

    @classmethod
    def list_users(cls) -> list[UserOut]:
        if not cls._users:
            cls._users = [
                UserOut(id=1, username="admin", full_name="Quản trị hệ thống", email="admin@example.com", role="admin", is_active=True),
                UserOut(id=2, username="member", full_name="Thành viên", email="member@example.com", role="member", is_active=True),
            ]
        return cls._users

    @classmethod
    def create_user(cls, payload: UserCreate) -> UserOut:
        user = UserOut(id=len(cls.list_users()) + 1, **payload.model_dump(), is_active=True)
        cls._users.append(user)
        return user
