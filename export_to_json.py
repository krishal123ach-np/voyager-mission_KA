import mysql.connector
import json
import os
from dotenv import load_dotenv

load_dotenv()
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("DB_PASSWORD"),
    database="voyager_mission",
    use_pure=True
)

cursor = db.cursor(dictionary=True)

cursor.execute("SELECT name, distance_parsecs, distance_ly, radius_earth, star_temp_k FROM exoplanets")
rows = cursor.fetchall()

print(f"pulled {len(rows)} planets from the database.")

with open("exoplanets.json", "w") as f:
    json.dump(rows, f, indent=2)

print("Wrote exoplanets.json")

cursor.close()
db.close()