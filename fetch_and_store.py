import requests
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
query = """
SELECT pl_name, sy_dist, pl_rade, st_teff
FROM ps
WHERE sy_dist IS NOT NULL
"""

url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
params = {"query": query, "format": "json"}

response = requests.get(url, params=params)
response.raise_for_status()
planets = response.json()
print(planets[0])
print(f"Fetched {len(planets)} planets from NASA.")

PARSECS_TO_LY = 3.26156
for p in planets:
    p["distance_ly"] = p["sy_dist"] * PARSECS_TO_LY

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("DB_PASSWORD"),
    database="voyager_mission",
    use_pure=True
)

cursor = db.cursor()
cursor.execute("SELECT DATABASE(), @@port;")
print(cursor.fetchone())


insert_query = """
INSERT INTO exoplanets (name, distance_parsecs, distance_ly, radius_earth, star_temp_k)
VALUES (%s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
    distance_parsecs = VALUES(distance_parsecs),
    distance_ly = VALUES(distance_ly),
    radius_earth = VALUES(radius_earth),
    star_temp_k = VALUES(star_temp_k)
"""

for p in planets:
    values = (p["pl_name"], p["sy_dist"], p["distance_ly"], p["pl_rade"], p["st_teff"])
    cursor.execute(insert_query, values)

db.commit()
print(f"Inserted {cursor.rowcount} row(s) in the last statement.")
print("All done! check your exoplanets table.")

cursor.close()
db.close()