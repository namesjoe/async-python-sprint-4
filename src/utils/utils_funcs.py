import random
import string

from src.models.model import pwd_context


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def generate_random_string(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def get_db_url(db_name: str, host_url: str) -> str:
    return f"{host_url}{db_name}"
