from pydantic import BaseSettings


class Settings(BaseSettings):
    FASTAPI_CONNECTION_STRING: str
    FASTAPI_SECRET_KEY: str


settings = Settings()
