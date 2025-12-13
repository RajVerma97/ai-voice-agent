from pydantic import BaseModel
from typing import Optional


class ScheduleRequest(BaseModel):
    title: Optional[str]
    author: str
    date: str
    time: str
