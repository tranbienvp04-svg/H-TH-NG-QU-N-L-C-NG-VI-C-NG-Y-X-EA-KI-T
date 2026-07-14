from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    full_name: str
    email: str | None = None
    role: str = "member"


class UserOut(BaseModel):
    id: int
    username: str
    full_name: str
    email: str | None = None
    role: str
    is_active: bool
