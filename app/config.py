from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "CSV Management API"
    APP_VERSION: str = "1.0.0"

    # PostgreSQL
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    ADMIN_EMAIL: str
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str

    ADMIN_FIRST_NAME: str = "System"
    ADMIN_LAST_NAME: str = "Admin"
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SMTP_FROM_EMAIL: str

    SMTP_PORT: int = 465 #587

    SMTP_HOST: str

    MAIL_FROM_NAME: str = "My App"

    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    FRONTEND_URL: str = "http://localhost:3000/"
    ENV: str = "development"
    



    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    @property
    def DATABASE_URL(self) -> str:
        if self.ENV =="development":
            return (
                f"postgresql+psycopg2://"
                f"{self.DATABASE_USER}:"
                f"{self.DATABASE_PASSWORD}@"
                f"{self.DATABASE_HOST}:"
                f"{self.DATABASE_PORT}/"
                f"{self.DATABASE_NAME}?sslmode=require"
            )
        return (
                        f"postgresql+psycopg2://"
                        f"{self.DATABASE_USER}:"
                        f"{self.DATABASE_PASSWORD}@"
                        f"{self.DATABASE_HOST}:"
                        f"{self.DATABASE_NAME}?sslmode=require"
                    )



@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
