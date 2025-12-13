from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date, time
from typing import List, Optional

app = FastAPI()


class ScheduleRequest(BaseModel):
    title: Optional[str]
    author: str
    date: str
    time: str


# create a post request that accepts title, date,time,name
@app.post("/event")
def create_meeting_event(request: ScheduleRequest):
    print("event is ", request)
    return {"event", request.date}
