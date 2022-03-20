from pydantic import BaseSettings


class Settings(BaseSettings):
    api_name: str = "Awesome API"
    database_url: str = "postgresql://user:password@127.0.0.1:5432/awesome-api"
    secret_key: str = "secret"


class HashSettings(BaseSettings):
    salt: str = "this is my salt"
    min_hash_length: int = 6
