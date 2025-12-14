from pydantic import BaseModel
from datetime import datetime



class CalendarEvent(BaseModel):
    title: str
    color_id: int
    description: str | None = None
    start_time: datetime
    end_time: datetime
    timezone: str
