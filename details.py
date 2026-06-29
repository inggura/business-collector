import os
import sqlite3
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
URL = "https://places.googleapis.com/v1/places/"

conn = sqlite3.connect("fortune.db")
cur = conn.cursor()

cur.execute("""
SELECT
    place_id,
    name
FROM places
WHERE phone IS NULL
""")

rows = cur.fetchall()

print(f"조회 대상 : {len(rows)}개")

for place_id, name in rows:

    response = requests.get(
        URL + place_id,
        headers={
            "X-Goog-Api-Key": API_KEY,
            "X-Goog-FieldMask":
                "nationalPhoneNumber,"
                "websiteUri,"
                "googleMapsUri,"
                "businessStatus"
        }
    )

    if response.status_code != 200:
        print(f"실패 : {name}")
        print(response.status_code)
        print(response.text)
        print("-" * 50)
        continue

    data = response.json()

    phone = data.get("nationalPhoneNumber")
    website = data.get("websiteUri")
    maps = data.get("googleMapsUri")
    status = data.get("businessStatus")

    cur.execute("""
    UPDATE places
    SET
        phone=?,
        website=?,
        google_maps_uri=?,
        business_status=?
    WHERE place_id=?
    """, (
        phone,
        website,
        maps,
        status,
        place_id
    ))

    conn.commit()

    print(f"완료 : {name}")

conn.close()

print("모든 업데이트 완료!")