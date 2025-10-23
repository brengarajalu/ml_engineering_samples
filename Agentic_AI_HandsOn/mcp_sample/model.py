from pydantic.v1 import BaseModel


class FlightInfo(BaseModel):
    airline: str
    price: str
    duration: str
    stops: str
    departure: str
    arrival: str