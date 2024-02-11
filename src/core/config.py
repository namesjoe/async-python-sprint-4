import os

from pydantic import PostgresDsn, BaseSettings

dotenv_path = os.path.join(os.path.dirname(__file__), "../../.env")
subnet_blacklist = ["10.0.0.0/8"]

class DBSettings(BaseSettings):
    postgres_user: str = "postgres"
    postgres_password: str
    postgres_server: str = "postgres"
    postgres_port: str = "5432"
    postgres_db: str = "postgres"
    postgres_db_test: str = "postgres_test"

    class Config:
        env_file = dotenv_path
        extra = "allow"


db_set = DBSettings()


class AppSettings(BaseSettings):
    class Config:
        extra = "allow"

    project_name: str = "ShortLink"
    project_host: str = "127.0.0.1"
    project_port: int = 8080
    postgres_user: str = "postgres"
    postgres_password: str
    postgres_server: str = "postgres"
    postgres_port: str = "5432"
    postgres_db: str = "postgres"
    postgres_db_test: str = "postgres_test"

    short_link_length: int = 6

    database_dsn: PostgresDsn = f"postgresql+asyncpg://{db_set.postgres_user}:"\
                                f"{db_set.postgres_password}@{db_set.postgres_server}:"\
                                f"{db_set.postgres_port}/{db_set.postgres_db}"

    database_test_dsn: PostgresDsn = f"postgresql+asyncpg://{db_set.postgres_user}:"\
                                     f"{db_set.postgres_password}@{db_set.postgres_server}:"\
                                     f"{db_set.postgres_port}/{db_set.postgres_db_test}"

    class Config:
        env_file = dotenv_path


app_settings = AppSettings()
