import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://sakila:p_ssW0rd@postgres:5432/sakila")

settings = Settings()