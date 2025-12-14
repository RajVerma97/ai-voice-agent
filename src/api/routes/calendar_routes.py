from fastapi import FastAPI, APIRouter
from src.api.handlers import CalendarHandler
from src.api.requests import CreateEventRequest

calendar_router = APIRouter(prefix="/calendar", tags=["calendar"])
calendar_handler = CalendarHandler()


@calendar_router.get("/events")
async def get_calendar_events(count: int):
    return calendar_handler.handle_get_events(count=count)


@calendar_router.post("/events")
async def create_event(request: CreateEventRequest):
    return calendar_handler.handle_create_event(request)
