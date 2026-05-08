from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Setting(BaseSettings):
    database_hostname: str
    database_username: str
    database_password: str
    database_name: str
    database_port: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = ConfigDict(env_file=".env")

settings = Setting()
