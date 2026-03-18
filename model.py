from pydantic import BaseModel, field_validator
import re

class Location(BaseModel):
    latitude: float|None
    longitude: float|None

    @field_validator("latitude")
    def validate_latitude(cls, v):
        if v is None:
            return v
        if not (-90 <= v <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        return v

    @field_validator("longitude")
    def validate_longitude(cls, v):
        if v is None:
            return v
        if not (-180 <= v <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        return v


class Availability(BaseModel):
    day: str|None
    time_range: str|None


class Items(BaseModel):
    item_name: str|None
    item_img: str | None
    price: float|None
    discount_price: float | None
    description: str|None

    @field_validator("price")
    def validate_price(cls, v):
        if v is None:
            return v
        if v < 0:
            raise ValueError("Price cannot be negative")
        return v


class Menu(BaseModel):
    category: str|None
    items: list[Items]


class GrabFood(BaseModel):
    restaurant_name: str|None
    product_category: str|None
    img: str|None
    location: Location
    timeZone: str|None
    currency: str|None
    delivery_time: str|None 
    rating: float | None
    availability: list[Availability]
    deliverable_distance: float|None
    menu: list[Menu]

    @field_validator("currency")
    def validate_currency(cls, v):
        if v is None:
            return v
        if not re.match(r"^[A-Z]{2,3}$", v):
            raise ValueError("Invalid currency code")
        return v

   