from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    BYEDPI_PATH: str = Field(..., env="BYEDPI_PATH")
    ARGS_FILE: str = Field(default="assets/args.txt", env="ARGS_PATH")
    HOSTS_FILE: str = Field(default="assets/hosts.txt", env="HOSTS_PATH")
    TIMEOUT: int = Field(default=3, env="TIMEOUT")
    PROXY_URL: str = Field(default="socks5://127.0.0.1:1080", env="PROXY_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
