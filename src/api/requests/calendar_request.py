from pydantic import BaseModel
from pydantic import Field, field_validator
from datetime import datetime
from typing import List
from src.schemas import CalendarEvent
from datetime import datetime, timezone, timedelta


class GetEventsRequest(BaseModel):
    count: int = Field(
        default=10, ge=1, le=100, description="Maximum number of events to return"
    )


class CreateEventRequest(BaseModel):
    """Request schema for creating a calendar event."""

    title: str = Field(..., min_length=1, max_length=200, description="Event title")
    author: str = Field(..., min_length=1, description="Event organizer/author")
    date: str = Field(..., description="Event date in YYYY-MM-DD format")
    time: str = Field(..., description="Event time in HH:MM format (24-hour)")
    duration_minutes: int = Field(
        default=60, ge=15, le=480, description="Event duration in minutes (default: 60)"
    )
    description: str | None = Field(
        None, max_length=1000, description="Event description"
    )
    location: str | None = Field(None, max_length=500, description="Event location")
    color_id: int = Field(default=9, ge=1, le=11, description="Calendar color (1-11)")

    @field_validator("date")
    @classmethod
    def validate_date(cls, v):
        """Validate date format and ensure it's not in the past."""
        try:
            event_date = datetime.strptime(v, "%Y-%m-%d").date()
            today = datetime.now().date()

            if event_date < today:
                raise ValueError("Cannot schedule events in the past")

            return v
        except ValueError as e:
            if "past" in str(e):
                raise e
            raise ValueError("Date must be in YYYY-MM-DD format (e.g., 2025-12-20)")

    @field_validator("time")
    @classmethod
    def validate_time(cls, v):
        """Validate time format."""
        try:
            datetime.strptime(v, "%H:%M")
            return v
        except ValueError:
            raise ValueError("Time must be in HH:MM format (24-hour, e.g., 15:30)")

    def convertCreateEventRequestToCalendarEvent(
        self, request: CreateEventRequest
    ) -> CalendarEvent:
        # 1. Parse date and time from strings
        event_datetime_str = f"{request.date} {request.time}"
        event_datetime = datetime.strptime(event_datetime_str, "%Y-%m-%d %H:%M")
        event_datetime = event_datetime.replace(tzinfo=timezone.utc)

        # 2. Calculate end time
        end_datetime = event_datetime + timedelta(minutes=request.duration_minutes)

        # 3. Convert CreateEventRequest -> CalendarEvent (domain model)
        calendar_event = CalendarEvent(
            title=request.title,
            description=request.description or f"Organized by {request.author}",
            start_time=event_datetime,
            end_time=end_datetime,
            timezone="UTC",
            color_id=request.color_id,
        )
        return calendar_event
