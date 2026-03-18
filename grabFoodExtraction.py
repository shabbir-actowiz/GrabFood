from pydantic import BaseModel,field_validator
import re
import json
from datetime import datetime,time,timedelta
import mysql.connector

class Location(BaseModel):
    latitude:float
    longitude:float

    @field_validator("latitude")
    def validate_latitude(cls, v):
        if not (-90 <= v <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        return v

    @field_validator("longitude")
    def validate_longitude(cls, v):
        if not (-180 <= v <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        return v

class Availability(BaseModel):
    day: str
    time_range: str   

class Items(BaseModel):
    item_name:str
    item_img:str | None
    price:float
    discount_price:float 
    description:str

    @field_validator("price")
    def validate_price(cls, v):
        if v < 0:
            raise ValueError("Price cannot be negative")
        return v

class Menu(BaseModel):
    category:str
    items:list[Items]

class UberEats(BaseModel):
    restaurant_name: str
    product_category:str
    product_img:str
    location:Location
    time_zone:str
    currency:str
    delivery_time:str
    rating:float | None
    availability:list[Availability]
    deliverable_distance:float
    menu:list[Menu]

    @field_validator("currency")
    def validate_currency(cls, v):
        if not re.match(r"^[A-Z]{2}$", v):
            raise ValueError("Invalid currency code")
        return v
    
    @field_validator('delivery_time', mode='before')
    def bedtype_to_int(cls, values):
        delivery_time = re.findall(r'\d+', values)
        return delivery_time[0] if delivery_time else 0


with open('grabFood.json','r',encoding='utf-8') as f:
    data=json.load(f)

try:
    data=data['merchant']
    restaurant_name=data['name']
    product_category=data['cuisine']
    product_img=data['photoHref']
    time_Zone=data['timeZone']
    location_path=data['latlng']
    location=Location(latitude=location_path['latitude'],longitude=location_path['longitude'])
    currency=data['currency']['symbol']
    delivery_time=data['deliveryETARange']
    rating=data['rating']
    deliverable_distance=data['distanceInKm']
    av=data['openingHours']
    days = {"sun", "mon", "tue", "wed", "thu", "fri", "sat"}

    availability_list = [
        {"day": day, "time_range": value}
        for day, value in av.items()
        if day in days
    ]
    
    menu_list=[]
    if 'menu' in data and 'categories' in data['menu']:
        for category in data['menu']['categories']:
            if category['name'].lower() == 'for you':
                continue
            items=[]
            if 'items' in category:
                for item in category['items']:
                    items.append(Items(
                        item_name=item['name'],
                        item_img=item.get('imgHref'),
                        price=item['priceV2']['amountDisplay'],
                        discount_price=item['discountedPriceV2']['amountDisplay'],
                        description=item['description']
                    ))
            menu_list.append(Menu(category=category['name'], items=items))
    
    uber_eats_data = UberEats(
        restaurant_name=restaurant_name,
        product_category=product_category,
        product_img=product_img,
        location=location,
        time_zone=time_Zone,
        currency=currency,
        delivery_time=delivery_time,
        rating=rating,
        availability=availability_list,
        deliverable_distance=float(deliverable_distance),
        menu=menu_list
    )


except Exception as e:
        print(f"Error extracting merchant data: {e}")

with open('grabFoodOutput.json', 'w', encoding='utf-8') as f:
    json.dump(uber_eats_data.model_dump(), f, ensure_ascii=False, indent=4)