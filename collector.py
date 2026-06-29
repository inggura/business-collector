import sqlite3
import time
import pandas as pd
from tqdm import tqdm
from google_places import search_places



conn = sqlite3.connect("fortune.db")
cur = conn.cursor()

regions = pd.read_csv("data/regions_all.csv")
keywords = pd.read_csv("data/keywords.csv")

BAD_WORDS = [
    "CU",
    "GS25",
    "세븐일레븐",
    "이마트",
    "롯데마트",
    "주민센터",
    "구청",
    "시청",
    "학교",
    "병원",
    "약국",
    "은행",
    "세무",
    "회계",
    "Toys",
    "Cafe",
    "Coffee",
    "Street",
    "Observatory",
    "Office",
    "Restaurant",
    "School",
    "Hospital"
    "Office"
]

GOOD_WORDS = [
    "점집",
    "신점",
    "사주",
    "타로",
    "철학관",
    "철학원",
    "명리",
    "역학",
    "작명",
    "운세",
    "보살",
    "신당",
    "도령",
    "선녀",
    "암",
    "정사",
    "궁",
    "법사",
    "무당"
]
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
            name = place["displayName"]["text"]
            print(name)
            print("-" * 50)



            if any(word.lower() in name.lower() for word in BAD_WORDS):
                print(f"제외 : {name}")
                continue
            if not any(word in name for word in GOOD_WORDS):
                print(f"무시 : {name}")
                continue
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
                name,
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