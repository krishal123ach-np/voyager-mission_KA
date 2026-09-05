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
cursor.execute("SELECT name, distance_ly, mass_solar FROM black_holes")
rows = cursor.fetchall()
print(f"EXPORTED {len(rows)} black holes.")
with open("black_holes.json", "w") as f:
    json.dump(rows, f, indent=2)

print("Exported black holes to black_holes.json")

cursor.close()
db.close()
