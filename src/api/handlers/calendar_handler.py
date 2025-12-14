from src.services import CalendarService
from src.schemas import CalendarEvent
from src.api.requests import CreateEventRequest, GetEventsRequest


class CalendarHandler:
    def __init__(self):
        self.calendar_service = CalendarService()

    def handle_get_events(self, request: GetEventsRequest):
        events = self.calendar_service.get_events(request.count)
        return {"events": events}

    def handle_create_event(self, request: CreateEventRequest):
        calendar_event_request = request.convertCreateEventRequestToCalendarEvent(
            request
        )
        return self.calendar_service.create_event(calendar_event_request)
