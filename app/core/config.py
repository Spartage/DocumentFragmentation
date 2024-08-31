import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Desafio Técnico Desarrollador FullStack Adereso"
    debug: bool = True
    version: str = "1.0.0"
    gpt_api_key: str = os.getenv("GPT_API_KEY", "")

    class Config:
        env_file = ".env"

settings = Settings()