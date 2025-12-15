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
from src.schemas import CalendarEvent
from .auth import GoogleAuthenticator
from .mappers import GoogleCalendarMapper
from src.config import Config


class GoogleCalendarClient:
    def __init__(
        self,
        credentials_file: str | None = None,
        token_file: str | None = None,
    ):
        self.credentials_file = (
            Path(credentials_file) if credentials_file else Config.CREDENTIALS_FILE
        )
        self.token_file = Path(token_file) if token_file else Config.TOKEN_FILE

        Config.ensure_config_dir()
        authenticator = GoogleAuthenticator(
            credentials_file=credentials_file,
            token_file=token_file,
            use_service_account=Config.USE_SERVICE_ACCOUNT,
        )
        self.credentials = authenticator._authenticate()
        self.service = build("calendar", "v3", credentials=self.credentials)
        self.mapper = GoogleCalendarMapper()

    def get_events(self, count: int) -> list[Dict] | None:
        logger.debug(f"Getting the upcoming {count} events")
        try:
            # Call the Calendar API
            now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
            events_result = (
                self.service.events()
                .list(
                    calendarId=Config.CALENDAR_ID,
                    timeMin=now,
                    maxResults=count,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])
            return events

        except HttpError as error:
            logger.error(f"failed to get upocoming event{error}")
            raise

    def create_event(self, event: CalendarEvent) -> Dict:
        logger.debug("Starting create event")
        try:
            calendar_event = self.mapper.domain_to_google_format(event)
            created_event = (
                self.service.events()
                .insert(calendarId=Config.CALENDAR_ID, body=calendar_event)
                .execute()
            )
            return created_event

        except HttpError as error:
            raise RuntimeError(f"Failed to create event: {error}")
