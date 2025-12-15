from pydantic import BaseModel
from typing import Optional, List


class EventPerson(BaseModel):
    email: str
    self: Optional[bool] = None


class EventDateTime(BaseModel):
    dateTime: str
    timeZone: str


class CalendarEvent(BaseModel):
    id: str
    status: str
    htmlLink: str
    summary: str
    description: Optional[str] = None
    colorId: Optional[str] = None
    creator: EventPerson
    organizer: EventPerson
    start: EventDateTime
    end: EventDateTime


class GetEventsResponse(BaseModel):
    events: List[CalendarEvent]


class CreateEventResponse(CalendarEvent):
    pass
