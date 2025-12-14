from fastapi import FastAPI, APIRouter, Depends
from src.api.handlers import CalendarHandler
from src.api.requests import CreateEventRequest, GetEventsRequest

calendar_router = APIRouter(prefix="/calendar", tags=["calendar"])
calendar_handler = CalendarHandler()


# get events
@calendar_router.get("/events")
async def get_calendar_events(request: GetEventsRequest = Depends()):
    return calendar_handler.handle_get_events(request)


# create event
@calendar_router.post("/events")
async def create_event(request: CreateEventRequest):
    return calendar_handler.handle_create_event(request)
