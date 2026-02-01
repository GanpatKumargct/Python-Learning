
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppConfig(BaseSettings):
    app_Name:str = "FASTAPI"
    app_env:str = "development"
    database_url:str

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache   
def get_app_config():
    return AppConfig() 