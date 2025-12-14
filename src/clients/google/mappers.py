"""Mappers for converting between domain models and Google Calendar API format."""

from typing import Dict
from datetime import datetime

from src.schemas import CalendarEvent
from src.utils.logger import logger


class GoogleCalendarMapper:
    """
    Converts between domain models and Google Calendar API format.

    Responsibilities:
    - CalendarEvent → Google API format
    - Google API response → Clean dictionary
    """

    @staticmethod
    def domain_to_google_format(event: CalendarEvent) -> Dict:
        """
        Convert CalendarEvent domain model to Google Calendar API format.

        Args:
            event: CalendarEvent domain model

        Returns:
            Dictionary in Google Calendar API format
        """
        google_event = {
            "summary": event.title,
            "description": event.description or "",
            "start": {
                "dateTime": event.start_time.isoformat(),
                "timeZone": event.timezone,
            },
            "end": {
                "dateTime": event.end_time.isoformat(),
                "timeZone": event.timezone,
            },
            "colorId": str(event.color_id),
        }

        logger.debug(f"Converted domain model to Google format: {event.title}")
        return google_event