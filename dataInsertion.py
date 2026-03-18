import mysql.connector
import json

with open('grabFoodOutput.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

conn=mysql.connector.connect(
    host='localhost',
    user='root',
    password='actowiz')
cursor=conn.cursor()
DB_NAME = "grab_food"


def create_database():
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")

def use_database():
    cursor.execute(f"USE {DB_NAME}")

def create_table():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS restaurant_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_name TEXT,
    product_category TEXT,
    product_img TEXT,
    
    latitude REAL,
    longitude REAL,
    
    time_zone TEXT,
    currency TEXT,
    delivery_time INTEGER,
    rating REAL,
    
    deliverable_distance REAL,
    
    availability TEXT,
    menu TEXT
    )
    """)

def insert_data():
    query = """
    INSERT INTO restaurant_data (
        restaurant_name,
        product_category,
        product_img,
        latitude,
        longitude,
        time_zone,
        currency,
        delivery_time,
        rating,
        deliverable_distance,
        availability,
        menu
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, (
        data["restaurant_name"],
        data["product_category"],
        data["product_img"],
        data["location"]["latitude"],
        data["location"]["longitude"],
        data["time_zone"],
        data["currency"],
        int(data["delivery_time"]),
        data["rating"],
        data["deliverable_distance"],
        json.dumps(data["availability"]),
        json.dumps(data["menu"])
    ))

    conn.commit()

if __name__ == "__main__":
    create_database()
    use_database()
    create_table()
    
    insert_data()
    conn.close()