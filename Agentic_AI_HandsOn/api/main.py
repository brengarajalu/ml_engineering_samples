from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# docs endpoint : http://127.0.0.1:8000/docs

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}

@app.post("/items/")
async def create_item(item: Item):
    return item

@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}

@app.get("/weather/{city}")
def get_weather(city: str):
    """Fetches weather for given city"""
    weather_data = { # Example data, use API in real-world
        "New York": "Sunny, 25°C",
        "London": "Cloudy, 18°C",
        "Tokyo": "Rainy, 22°C"
        }
    return weather_data.get(city, "Weather data not available.")