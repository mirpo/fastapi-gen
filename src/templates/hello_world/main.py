import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info("Starting up FastAPI application")
    yield
    logger.info("Shutting down FastAPI application")

app = FastAPI(
    title="Hello World API",
    description="A simple FastAPI example with common patterns",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # `.env.prod` takes priority over `.env_dev`
        env_file=(".env_dev", ".env.prod"),
    )
    api_version: str

settings = Settings()
load_dotenv(".env_dev")

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Item name")
    description: str | None = Field(None, max_length=500, description="Item description")
    price: float = Field(..., gt=0, description="Item price must be positive")
    tax: float | None = Field(None, ge=0, description="Tax amount")

class ItemResponse(BaseModel):
    item_id: int
    name: str
    description: str | None
    price: float
    tax: float | None


@app.get("/", tags=["root"])
async def root():
    """
    Example how use GET and return JSON
    """
    return {"message": "Hello World"}

@app.get("/health", tags=["health"], status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/version-pydantic-settings", tags=["config"])
async def version_pydantic_settings():
    """
    Example how use GET env variables using pydantic-settings package
    """
    return {"package": "pydantic-settings", "version": settings.api_version}

@app.get("/version-dotenv", tags=["config"])
async def version_dotenv():
    """
    Example how use GET env variables using dotenv package
    """
    return {"package": "dotenv", "version": os.getenv("API_VERSION")}

@app.post("/items/", tags=["items"], status_code=status.HTTP_201_CREATED)
async def create_item(item: Item) -> Item:
    """
    Example how use POST and return Typed JSON
    """
    logger.info(f"Creating item: {item.name}") # noqa: G004
    return item


@app.put("/items/{item_id}", tags=["items"], response_model=ItemResponse)
async def update_item(item_id: int, item: Item):
    """
    Example how use PUT
    """
    if item_id <= 0:
        raise HTTPException(status_code=400, detail="Item ID must be positive")

    logger.info(f"Updating item {item_id}: {item.name}") # noqa: G004
    return ItemResponse(item_id=item_id, **item.model_dump())


@app.get("/items/{item_id}", tags=["items"])
async def read_item(item_id: int, q: str | None = None):
    """
    Example how to read path and query parameters
    """
    if item_id <= 0:
        raise HTTPException(status_code=400, detail="Item ID must be positive")

    logger.info(f"Reading item {item_id}") # noqa: G004
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc): # noqa: ARG001
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code},
    )
