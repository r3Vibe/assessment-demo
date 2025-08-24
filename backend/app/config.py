import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    DB_URL: str = os.getenv("DB_URL")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")


try:
    settings = Settings()
except Exception as e:
    print(f"Config validation error: {e}")
    raise
