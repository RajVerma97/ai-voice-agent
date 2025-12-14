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

    @staticmethod
    def google_to_dict(google_event: Dict) -> Dict:
        """
        Convert Google Calendar API response to clean dictionary.

        Args:
            google_event: Raw event from Google Calendar API

        Returns:
            Cleaned event dictionary
        """
        return {
            "id": google_event.get("id"),
            "title": google_event.get("summary", "No Title"),
            "description": google_event.get("description"),
            "location": google_event.get("location"),
            "status": google_event.get("status", "confirmed"),
            "html_link": google_event.get("htmlLink"),
            "start": google_event.get("start"),
            "end": google_event.get("end"),
            "created": google_event.get("created"),
            "updated": google_event.get("updated"),
            "organizer": google_event.get("organizer", {}),
            "attendees": google_event.get("attendees", []),
            "color_id": google_event.get("colorId"),
        }
