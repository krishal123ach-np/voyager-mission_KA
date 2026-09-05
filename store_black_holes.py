import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()
black_holes = [
    ("Gaia BH1", 1560, 9.8),
    ("V616 Monocerotis", 3300, 6.6),
    ("Gaia BH2", 3800, 8.94),
    ("Cygnus X-1", 7200, 21.2),
    ("Sagittarius A*", 26000, 4300000),
    ("Gaia BH3", 1936, 32.7),
    ("OGLE-2011-BLG-0462", 5200, 7.1),
    ("V404 Cygni", 7800, 9.0),
    ("GS 2000+25", 8800, 7.5),
    ("MAXI J1820+070", 10000, 8.5),
    ("GRO J1655-40", 11000, 6.3),
    ("XTE J1550-564", 17000, 9.1),
    ("4U 1543-47", 24000, 9.4),
]

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("DB_PASSWORD"),
    database="voyager_mission",
    use_pure=True
)
cursor = db.cursor()

insert_query = """INSERT INTO black_holes (name, distance_ly, mass_solar) VALUES (%s, %s, %s) AS new_row
ON DUPLICATE KEY UPDATE
    distance_ly = new_row.distance_ly,
    mass_solar = new_row.mass_solar
"""
for bh in black_holes:
    cursor.execute(insert_query, bh)

db.commit()
print(f"STORED {len(black_holes)} black holes.")
cursor.close()
db.close()