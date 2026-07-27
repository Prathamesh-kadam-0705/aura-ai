from pathlib import Path
from dotenv import load_dotenv, dotenv_values
import os

BASE_DIR = Path(__file__).resolve().parents[2]   # aura-ai/
env_path = BASE_DIR / ".env"

print("ENV PATH:", env_path)
print("FILE EXISTS:", env_path.exists())
print("RAW ENV:", dotenv_values(env_path))

load_dotenv(env_path, override=True)

print("DB_HOST:", os.getenv("DB_HOST"))
print("DB_PORT:", os.getenv("DB_PORT"))
print("DB_USER:", os.getenv("DB_USER"))
print("DB_PASSWORD:", os.getenv("DB_PASSWORD"))


class Settings:
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")


settings = Settings()