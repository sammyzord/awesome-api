from pydantic import BaseSettings


class Settings(BaseSettings):
    api_name: str = "Awesome API"
    database_url: str = "postgresql://user:password@127.0.0.1:5432/awesome-api"
