import os
from pathlib import Path


class Config:
    # Base directory is project root
    BASE_DIR = Path(__file__).resolve().parent.parent

    USE_SERVICE_ACCOUNT = os.getenv("USE_SERVICE_ACCOUNT", "false").lower() == "true"

    # Credential file paths
    SERVICE_ACCOUNT_FILE = BASE_DIR / "service-account.json"
    CREDENTIALS_FILE = BASE_DIR / "credentials.json"
    TOKEN_FILE = BASE_DIR / "token.json"

    CALENDAR_ID = os.getenv("CALENDAR_ID", "primary")
    OAUTH_REDIRECT_PORT = int(os.getenv("OAUTH_REDIRECT_PORT", "8080"))

    @classmethod
    def ensure_config_dir(cls):
        """Ensure config directory exists"""
        cls.BASE_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def validate_credentials(cls):
        """Validate that required credential files exist"""
        if cls.USE_SERVICE_ACCOUNT:
            if not cls.SERVICE_ACCOUNT_FILE.exists():
                raise FileNotFoundError(
                    f"Service account file not found: {cls.SERVICE_ACCOUNT_FILE}"
                )
        else:
            if not cls.CREDENTIALS_FILE.exists():
                raise FileNotFoundError(
                    f"Credentials file not found: {cls.CREDENTIALS_FILE}"
                )
