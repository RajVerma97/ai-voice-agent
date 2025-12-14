from src.clients import GoogleCalendarClient
from src.schemas import CalendarEvent
from src.utils import logger
from src.api.requests import CreateEventRequest


class CalendarService:
    def __init__(self):
        logger.debug("Calendar Service")
        self.google_calendar_client = GoogleCalendarClient()

    def get_events(self, count: int):
        return self.google_calendar_client.get_upcoming_event(count=count)

    def create_event(self, request: CalendarEvent):
        return self.google_calendar_client.create_event(request)
