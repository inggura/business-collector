import os
import sqlite3
import time
import requests
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
from google_places import search_places

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

URL = "https://places.googleapis.com/v1/places:searchText"

HEADERS = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": API_KEY,
    "X-Goog-FieldMask":
        "places.id,"
        "places.displayName,"
        "places.formattedAddress,"
        "places.location,"
        "places.rating,"
        "places.userRatingCount"
}

conn = sqlite3.connect("fortune.db")
cur = conn.cursor()

regions = pd.read_csv("data/regions_all.csv")
keywords = pd.read_csv("data/keywords.csv")

print("=" * 50)
print(f"검색 지역 수 : {len(regions)}")
print(f"키워드 수 : {len(keywords)}")
print(f"예상 검색 횟수 : {len(regions) * len(keywords)}")
print("=" * 50)


for _, r in tqdm(
    regions.iterrows(),
    total=len(regions),
    desc="지역"
):

    region = r["region"]

    for _, k in keywords.iterrows():

        keyword = k["keyword"]

        query = f"{region} {keyword}"

        print(f"\n검색 : {query}")

        places = search_places(query)

        if not places:
            print("검색 결과 없음")
            continue

        saved = 0
        duplicate = 0

        for place in places:
            cur.execute("""
            INSERT OR IGNORE INTO places
            (
                place_id,
                name,
                address,
                latitude,
                longitude,
                rating,
                reviews,
                keyword,
                region
            )
            VALUES(?,?,?,?,?,?,?,?,?)
            """, (
                place.get("id"),
                place["displayName"]["text"],
                place.get("formattedAddress"),
                place.get("location", {}).get("latitude"),
                place.get("location", {}).get("longitude"),
                place.get("rating"),
                place.get("userRatingCount"),
                keyword,
                region
            ))

            if cur.rowcount == 1:
                saved += 1
            else:
                duplicate += 1

        conn.commit()

        print(
            f"조회 {len(places)}개 | "
            f"신규 {saved}개 | "
            f"중복 {duplicate}개"
        )

        time.sleep(1)


conn.close()

print("\n완료")