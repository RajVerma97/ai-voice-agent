import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleCalendarEvent:
    SCOPES = ["https://www.googleapis.com/auth/calendar"]

    def __init__(
        self,
        credentials_file: str = "credentials.json",
        token_file: str = "token.json",
    ):
        self.credentials = self.__authenticate()
        self.service = build("calendar", "v3", credentials=self.credentials)

    def __authenticate(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.SCOPES
                )
                creds = flow.run_local_server(port=8000)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return creds

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

    def add_event(
        self,
        title: str,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        color_id: int,
        timezone: str = "UTC",
        description: str | None = None,
    ):
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
            return created_event

        except HttpError as error:
            raise RuntimeError(f"Failed to create event: {error}")


google_calendar_event = GoogleCalendarEvent()
# google_calendar_event.get_upcoming_event()

start = datetime.datetime(2025, 1, 10, 15, 20, tzinfo=datetime.timezone.utc)
end = datetime.datetime(2025, 1, 10, 16, 4, tzinfo=datetime.timezone.utc)


event = google_calendar_event.add_event(
    title="AI Interview Call",
    start_time=start,
    end_time=end,
    color_id=6,
    timezone="Asia/Kolkata",
    description="Scheduled via voice assistant",
)

print("Event created:", event["htmlLink"])
