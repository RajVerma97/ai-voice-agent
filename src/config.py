import os
from pathlib import Path


# config.py - Centralized configuration
class Config:
    # Base directory is project root
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Config directory
    CONFIG_DIR = BASE_DIR / "config"

    # Google credentials paths
    CREDENTIALS_FILE = CONFIG_DIR / "credentials.json"
    TOKEN_FILE = CONFIG_DIR / "token.json"

    OAUTH_REDIRECT_PORT = int(os.getenv("OAUTH_REDIRECT_PORT", "8080"))

    @classmethod
    def ensure_config_dir(cls):
        """Ensure config directory exists"""
        cls.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
