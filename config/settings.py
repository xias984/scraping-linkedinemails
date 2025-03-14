import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente
load_dotenv()

class Settings:
    LOGIN_URL = f"{os.getenv("BASE_URL")}/login"

    # Credenziali dal file .env
    EMAIL = os.getenv("EMAIL_KOALA")
    PASSWORD = os.getenv("PASSWORD_KOALA")

    # Timeout per Selenium
    DEFAULT_TIMEOUT = 10

    # Nome del database SQLite
    DB_NAME = os.getenv("DB_NAME", "linkedin_data.db")
