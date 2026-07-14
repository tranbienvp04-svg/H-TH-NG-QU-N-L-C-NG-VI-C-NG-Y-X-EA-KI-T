from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "Quản lý công việc Đảng ủy"
    DEBUG: bool = True
    SECRET_KEY: str = "dev-secret"
    DATABASE_URL: str = "sqlite:///./app.db"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480


settings = Settings()
