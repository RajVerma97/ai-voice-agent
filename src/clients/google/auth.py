import os
from pathlib import Path
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from src.utils.logger import logger
from src.config import Config


class GoogleAuthenticator:
    SCOPES = ["https://www.googleapis.com/auth/calendar"]

    def __init__(
        self,
        use_service_account: bool,
        credentials_file: str | None = None,
        token_file: str | None = None,
    ):
        # Determine auth method from config if not specified
        self.use_service_account = (
            use_service_account
            if use_service_account is not None
            else Config.USE_SERVICE_ACCOUNT
        )

        # Use appropriate credentials file based on auth method
        if self.use_service_account:
            self.credentials_file = (
                Path(credentials_file)
                if credentials_file
                else Config.SERVICE_ACCOUNT_FILE
            )
        else:
            self.credentials_file = (
                Path(credentials_file) if credentials_file else Config.CREDENTIALS_FILE
            )

        self.token_file = Path(token_file) if token_file else Config.TOKEN_FILE

        Config.ensure_config_dir()

        # Don't authenticate at init - lazy load instead
        self._credentials = None

    @property
    def credentials(self):
        """Lazy load credentials only when needed"""
        if self._credentials is None:
            self._credentials = self._authenticate()
        return self._credentials

    def _authenticate(self):
        """
        Authenticate with Google Calendar API.
        Uses service account in production, OAuth in development.
        """
        if self.use_service_account:
            return self._authenticate_service_account()
        else:
            return self._authenticate_oauth()

    def _authenticate_service_account(self):
        """
        Authenticate using service account (for production).
        Service accounts don't require user interaction.
        """
        logger.info("Authenticating with service account")

        try:
            credentials = service_account.Credentials.from_service_account_file(
                str(self.credentials_file), scopes=self.SCOPES
            )
            logger.info("Successfully authenticated with service account")
            return credentials
        except Exception as e:
            logger.exception("Failed to authenticate with service account")
            raise

    def _authenticate_oauth(self):
        """
        Authenticate using OAuth (for development/personal use).
        Requires user interaction on first run.
        """
        logger.debug("Starting OAuth authentication")
        creds = None

        try:
            # Load existing credentials if available
            if self.token_file.exists():
                creds = Credentials.from_authorized_user_file(
                    str(self.token_file), self.SCOPES
                )
                logger.debug("Loaded existing OAuth credentials")

            # Refresh or create new credentials
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    logger.debug("Refreshing expired credentials")
                    creds.refresh(Request())
                else:
                    logger.warning(
                        "No valid credentials found. OAuth flow requires user interaction."
                    )
                    logger.info(
                        "Run authentication separately before starting the server, "
                        "or use service account for production."
                    )
                    flow = InstalledAppFlow.from_client_secrets_file(
                        str(self.credentials_file), self.SCOPES
                    )
                    creds = flow.run_local_server(port=Config.OAUTH_REDIRECT_PORT)

                # Save credentials for future use
                self.token_file.write_text(creds.to_json())
                logger.debug("OAuth credentials saved successfully")

            logger.info("Successfully authenticated with OAuth")
            return creds

        except Exception as e:
            logger.exception("Failed to authenticate with OAuth")
            raise
