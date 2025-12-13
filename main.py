from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import datetime
from typing import List, Optional
from google_calendar_client import GoogleCalendarClient
from zoneinfo import ZoneInfo
from schemas import ScheduleRequest
from utils.logger import logger
from config import event_config

app = FastAPI()


def build_start_end(date_str: str, time_str: str, duration_min: int = 30):
    local_tz = ZoneInfo(event_config.calendar_timezone)

    start_local = datetime.datetime.strptime(
        f"{date_str} {time_str}", "%Y-%m-%d %H:%M"
    ).replace(tzinfo=local_tz)

    end_local = start_local + datetime.timedelta(minutes=duration_min)

    return (
        start_local.astimezone(datetime.timezone.utc),
        end_local.astimezone(datetime.timezone.utc),
    )


async def create_event(req: ScheduleRequest):
    google_calendar_event = GoogleCalendarClient()

    start, end = build_start_end(
        req.date, req.time, event_config.default_event_duration_minutes
    )
    meeting_title = req.title or event_config.default_event_title

    event = google_calendar_event.create_event(
        title=meeting_title,
        start_time=start,
        end_time=end,
        color_id=event_config.calendar_color_id,
        timezone=event_config.calendar_timezone,
        description="Scheduled via voice assistant",
    )
    logger.info(
        f"Successfully inserted event in the calendar with title:{meeting_title}"
    )
    return event


@app.post("/event")
async def create_meeting_event(request: ScheduleRequest):
    logger.info(f"Creating Event....")
    try:
        response = await create_event(request)
        event_link = response["htmlLink"]
        return {"status": "success", "event_link": event_link}
    except Exception as error:
        raise HTTPException(status_code=500, detail="failed to create event")
