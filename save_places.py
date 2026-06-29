import sqlite3
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

url = "https://places.googleapis.com/v1/places:searchText"

headers = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": API_KEY,
    "X-Goog-FieldMask": "places.displayName,places.formattedAddress"
}

data = {
    "textQuery": "서울 강남구 점집"
}

response = requests.post(url, headers=headers, json=data)

places = response.json()["places"]

conn = sqlite3.connect("fortune.db")
cur = conn.cursor()

for place in places:

    name = place["displayName"]["text"]
    address = place["formattedAddress"]

    cur.execute(
        """
        INSERT INTO places(name,address,keyword,region)
        VALUES(?,?,?,?)
        """,
        (
            name,
            address,
            "점집",
            "서울 강남구"
        )
    )

conn.commit()
conn.close()

print("저장 완료")