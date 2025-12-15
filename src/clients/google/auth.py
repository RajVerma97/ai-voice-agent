import datetime
import os.path
from typing import Optional, List, Dict, Any
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from src.utils.logger import logger
from src.config import Config


class GoogleAuthenticator:
    SCOPES = ["https://www.googleapis.com/auth/calendar"]

    def __init__(
        self,
        credentials_file: str | None = None,
        token_file: str | None = None,
    ):
        # Use Config defaults if not provided
        self.credentials_file = (
            Path(credentials_file) if credentials_file else Config.CREDENTIALS_FILE
        )
        self.token_file = Path(token_file) if token_file else Config.TOKEN_FILE

        # Ensure config directory exists
        Config.ensure_config_dir()

        self.credentials = self._authenticate()

    def _authenticate(self):
        """
        Authenticate with Google Calendar API.

        Returns:
            Credentials object for API access

        Raises:
            Exception: If authentication fails
        """
        logger.debug("Starting Google Calendar authentication")
        creds = None

        try:
            # Load existing credentials if available
            if self.token_file.exists():
                creds = Credentials.from_authorized_user_file(
                    str(self.token_file), self.SCOPES
                )

            # Refresh or create new credentials
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    logger.debug("Refreshing expired credentials")
                    creds.refresh(Request())
                else:
                    logger.debug("Running OAuth flow for new authentication")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        str(self.credentials_file), self.SCOPES
                    )
                    creds = flow.run_local_server(port=Config.OAUTH_REDIRECT_PORT)

                # Save credentials for future use
                self.token_file.write_text(creds.to_json())
                logger.debug("Credentials saved successfully")

            logger.info("Successfully authenticated with Google Calendar")
            return creds

        except Exception as e:
            logger.exception("Failed to authenticate with Google Calendar")
            raise
