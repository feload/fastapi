from pydantic import BaseSettings


class Settings(BaseSettings):
    FASTAPI_CONNECTION_STRING: str
    FASTAPI_SECRET_KEY: str
    FASTAPI_AUTH_ALGORITHM: str
    FASTAPI_ACCESS_TOKEN_EXPIRATION_MINUTES: int

    class Config():
        env_file: str = ".env"


settings = Settings()
