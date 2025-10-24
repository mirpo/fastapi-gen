import datetime
import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import BackgroundTasks, Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

app = FastAPI()


class CustomError(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(CustomError)
async def custom_exception_handler(_request: Request, exc: CustomError):
    """
    Custom exception handler example
    """
    return JSONResponse(
        status_code=418,
        content={"message": f"Custom error occurred: {exc.name}"},
    )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # `.env.prod` takes priority over `.env_dev`
        env_file=(".env_dev", ".env.prod"),
    )
    api_version: str


settings = Settings()
load_dotenv(".env_dev")


def get_settings():
    """
    Dependency to get settings instance
    """
    return settings


def write_log(message: str):
    """
    Background task to write log message
    """
    with open("app.log", "a") as log_file:
        log_file.write(f"{datetime.datetime.now(datetime.UTC)}: {message}\n")


class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Item name")
    description: str | None = Field(None, max_length=500, description="Item description")
    price: float = Field(..., gt=0, description="Item price must be greater than 0")
    tax: float | None = Field(None, ge=0, le=100, description="Tax percentage (0-100)")


@app.get("/")
async def root():
    """
    Example how use GET and return JSON
    """
    return {"message": "Hello World"}


@app.get("/health")
async def health_check():
    """
    Health check endpoint with timestamp
    """
    return {"status": "healthy", "timestamp": datetime.datetime.now(datetime.UTC)}


@app.get("/version-pydantic-settings")
async def version_pydantic_settings():
    """
    Example how use GET env variables using pydantic-settings package
    """
    return {"package": "pydantic-settings", "version": settings.api_version}


@app.get("/version-dotenv")
async def version_dotenv():
    """
    Example how use GET env variables using dotenv package
    """
    return {"package": "dotenv", "version": os.getenv("API_VERSION")}


@app.get("/config")
async def get_config(settings: Annotated[Settings, Depends(get_settings)]):
    """
    Example how to use dependency injection with settings
    """
    return {"api_version": settings.api_version, "source": "dependency_injection"}


@app.post("/items/")
async def create_item(item: Item) -> Item:
    """
    Example how use POST and return Typed JSON
    """
    return item


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    """
    Example how use PUT
    """
    return {"item_id": item_id, **item.model_dump()}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    """
    Example how to read path and query parameters
    """
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


@app.post("/send-notification/")
async def send_notification(background_tasks: BackgroundTasks):
    """
    Example how to use background tasks
    """
    background_tasks.add_task(write_log, "notification sent")
    return {"message": "Notification sent in background"}


@app.get("/error-example")
async def error_example(*, trigger_error: bool = False):
    """
    Example endpoint that can trigger custom exception
    """
    if trigger_error:
        msg = "example error"
        raise CustomError(msg)
    return {"message": "No error occurred"}
