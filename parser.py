import json
import gzip
from model import GrabFood, Location, Menu, Items
from db import OUTPUT_FOLDER_PATH

def parse_file(file_path):
    with gzip.open(file_path, 'rt',encoding='utf-8') as f_in:
        raw = json.load(f_in)

    try:
        if raw.get('merchant') is not None:
            data = raw['merchant']
        else:
            print(f"No merchant data found in {file_path}")
            return GrabFood(
        restaurant_name=None,
        product_category=None,
        img=None,
        location=Location(latitude=0.0, longitude=0.0),
        timeZone=None,
        currency=None,
        delivery_time=None,
        rating=None,
        availability=[],
        deliverable_distance=None,
        menu=[]
    )

        location = Location(
            latitude=data.get('latlng', {}).get('latitude'),
            longitude=data.get('latlng', {}).get('longitude')
        )

        availability_list = []
        if "openingHours" in data:
            days = {"sun", "mon", "tue", "wed", "thu", "fri", "sat"}
            availability_list = [
                {"day": day, "time_range": value}
                for day, value in data["openingHours"].items()
                if day in days
            ]

        menu_list = []
        if "menu" in data and "categories" in data["menu"]:
            for menu in data["menu"]['categories']:
                if menu["name"].lower() == "for you":
                    continue

                items = []
                for item in menu.get("items", []):
                    items.append(Items(
                        item_name=item.get("name", ""),
                        item_img=item.get('imgHref',''),
                        price=item['priceV2']['amountDisplay'],
                        discount_price=item.get("discountedPriceV2", {}).get("amountDisplay"),
                        description=item.get("description", "")
                    ))

                menu_list.append(Menu(category=menu["name"], items=items))

        grab_food = GrabFood(
            restaurant_name=data.get('name',''),
            product_category=data.get('cuisine',''),
            img=data.get('photoHref',''),
            location=location,
            timeZone=data.get('timeZone',''),
            currency=data['currency']['symbol'],
            delivery_time=data.get('deliveryETARange', 'N/A'),
            rating=data.get('rating', None),
            availability=availability_list,
            deliverable_distance=data['distanceInKm'],
            menu=menu_list
        )

        # with open(f"{OUTPUT_FOLDER_PATH}/{data['name']}_output.json", 'w', encoding='utf-8') as f:
        #     json.dump(grab_food.model_dump(), f, ensure_ascii=False, indent=4)
        
        return grab_food

    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None  