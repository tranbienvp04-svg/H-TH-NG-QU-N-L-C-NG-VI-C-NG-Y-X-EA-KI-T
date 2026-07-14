from app.schemas.auth import LoginRequest, TokenResponse


class AuthService:
    @staticmethod
    def login(payload: LoginRequest) -> TokenResponse:
        if payload.username == "admin" and payload.password == "123456":
            return TokenResponse(
                access_token="demo-token",
                user={
                    "id": 1,
                    "username": "admin",
                    "full_name": "Quản trị hệ thống",
                    "email": "admin@example.com",
                    "role": "admin",
                    "is_active": True,
                },
            )
        raise ValueError("invalid_credentials")
