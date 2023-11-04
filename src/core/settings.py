from pydantic import BaseSettings


class Settings(BaseSettings):
    SERVER_HOST: str
    SERVER_PORT: int
    JWT_SECRET_KEY: str
    DBNAME: str
    HOST_URL: str

    class Config:
        env_file = ".env"
