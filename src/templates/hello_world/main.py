import os

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

app = FastAPI()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # `.env.prod` takes priority over `.env_dev`
        env_file=(".env_dev", ".env.prod"),
    )
    api_version: str

settings = Settings()
load_dotenv(".env_dev")

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.get("/")
async def root():
    """
    Example how use GET and return JSON
    """
    return {"message": "Hello World"}

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
