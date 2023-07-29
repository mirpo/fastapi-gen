from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


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
