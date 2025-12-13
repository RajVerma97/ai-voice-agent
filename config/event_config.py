from dataclasses import dataclass


@dataclass
class EventConfig:
    calendar_color_id: int = 6
    calendar_timezone: str = "Asia/Kolkata"
    default_event_title: str = "Demo Meeting"
    default_event_duration_minutes: int = 30


event_config = EventConfig()
