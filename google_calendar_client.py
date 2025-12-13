import datetime
import os.path
from typing import Optional, List, Dict, Any
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from utils.logger import logger
from config import event_config


class GoogleCalendarClient:
    SCOPES = ["https://www.googleapis.com/auth/calendar"]

    def __init__(
        self,
        credentials_file: str = "credentials.json",
        token_file: str = "token.json",
    ):
        self.credentials_file = Path(credentials_file)
        self.token_file = Path(token_file)
        self.credentials = self._authenticate()
        self.service = build("calendar", "v3", credentials=self.credentials)

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
                    creds = flow.run_local_server(port=0)

                # Save credentials for future use
                self.token_file.write_text(creds.to_json())
                logger.debug("Credentials saved successfully")

            logger.info("Successfully authenticated with Google Calendar")
            return creds

        except Exception as e:
            logger.exception("Failed to authenticate with Google Calendar")
            raise

    def get_upcoming_event(self, max_result: int = 10):
        try:
            # Call the Calendar API
            now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
            print("Getting the upcoming 10 events")
            events_result = (
                self.service.events()
                .list(
                    calendarId="primary",
                    timeMin=now,
                    maxResults=max_result,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])

            if not events:
                print("No upcoming events found.")
                return

            # Prints the start and name of the next 10 events
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                print(start, event["summary"])

        except HttpError as error:
            print(f"An error occurred: {error}")

    def create_event(
        self,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        color_id: int,
        title: str,
        timezone: str = "UTC",
        description: str | None = None,
    ):
        logger.debug("Starting create event")
        try:
            event = {
                "summary": title,
                "location": "Somewhere online",
                "description": description,
                "start": {
                    "dateTime": start_time.isoformat(),
                    "timeZone": timezone,
                },
                "end": {
                    "dateTime": end_time.isoformat(),
                    "timeZone": timezone,
                },
                "colorId": color_id,
                "attendees": [
                    {"email": "user1@gmail.com"},
                    {"email": "user2@gmail.com"},
                    {"email": "user3@gmail.com"},
                ],
            }
            created_event = (
                self.service.events().insert(calendarId="primary", body=event).execute()
            )
            logger.debug("Successfully Created event")
            return created_event

        except HttpError as error:
            raise RuntimeError(f"Failed to create event: {error}")
