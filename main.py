from fastapi import FastAPI
from src.api.routes import calendar_router
from uvicorn import run
from src.utils.logger import logger

app = FastAPI()

app.include_router(calendar_router)


@app.get("/health")
async def health():
    return {"status": "health"}


if __name__ == "__main__":
    logger.info("Starting uvicorn server...")
    run("main:app", host="0.0.0.0", port=8000)
