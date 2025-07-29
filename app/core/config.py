from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"
    PROJECT_NAME: str

    DEBUG: bool = True
    ALLOWED_ORIGINS: List[str] = ["*"]
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"

    REDIS_URL: str = "redis://localhost:6379/0"

    STORAGE_BACKEND: str = "local"
    IPFS_API_URL: str = "http://127.0.0.1:5001"

    WEB3_AUTH_PROVIDER_URL: str = ""
    MORALIS_API_KEY: str = ""

    # model_config = SettingsConfigDict(env_file=".env.test") # for testing
    model_config = SettingsConfigDict(env_file=".env") # in production   

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

settings = Settings()