import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    ADMIN_TELEGRAM_ID = int(os.getenv("ADMIN_TELEGRAM_ID", 0))
    IG_USERNAME = os.getenv("IG_USERNAME")
    IG_PASSWORD = os.getenv("IG_PASSWORD")
    DOMAIN = os.getenv("DOMAIN")
    PORT = int(os.getenv("PORT", 8080))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def validate(cls):
        required = [
            "TELEGRAM_BOT_TOKEN",
            "ADMIN_TELEGRAM_ID",
            "DOMAIN"
        ]
        missing = [key for key in required if not getattr(cls, key)]
        if missing:
            raise ValueError(f"Missing environment variables: {', '.join(missing)}")
