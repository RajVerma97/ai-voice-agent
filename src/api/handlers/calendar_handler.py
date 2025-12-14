from src.services import CalendarService
from src.schemas import CalendarEvent
from src.api.requests import CreateEventRequest


class CalendarHandler:
    def __init__(self):
        self.calendar_service = CalendarService()

    def handle_get_events(self, count: int):
        return self.calendar_service.get_events(count)

    def handle_create_event(self, request: CreateEventRequest):
        calendar_event_request = request.convertCreateEventRequestToCalendarEvent(
            request
        )
        return self.calendar_service.create_event(calendar_event_request)
