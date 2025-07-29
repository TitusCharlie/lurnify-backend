from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import psycopg2
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

load_dotenv()  # if you're using .env

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
    
    def create_database_if_not_exists(self):
        try:
            # Connect to default 'postgres' db
            con = psycopg2.connect(
                dbname=self.POSTGRES_DB,
                user=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_HOST,
                port=self.POSTGRES_PORT
            )
            con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

            cur = con.cursor()

            # Check if database exists
            cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{self.POSTGRES_DB}';")
            exists = cur.fetchone()

            if not exists:
                cur.execute(f"CREATE DATABASE {self.POSTGRES_DB};")
                print(f"Database '{self.POSTGRES_DB}' created successfully.")
            else:
                print(f"Database '{self.POSTGRES_DB}' already exists.")

            cur.close()
            con.close()
        except Exception as e:
            print(f"Error creating database: {e}")


settings = Settings()
settings.create_database_if_not_exists()