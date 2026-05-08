from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Database connection parameters
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    
    # JWT Authentication configuration
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        # Construct the database URL for SQLAlchemy
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

settings = Settings()
