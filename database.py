import sqlite3

conn = sqlite3.connect("fortune.db")
cur = conn.cursor()

# 1. 테이블 생성
cur.execute("""
CREATE TABLE IF NOT EXISTS places(
    place_id TEXT PRIMARY KEY,
    name TEXT,
    address TEXT,
    latitude REAL,
    longitude REAL,
    rating REAL,
    reviews INTEGER,

    phone TEXT,
    website TEXT,
    google_maps_uri TEXT,
    business_status TEXT,

    keyword TEXT,
    region TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")


# 2. 인덱스 생성
cur.execute("""
CREATE INDEX IF NOT EXISTS idx_region
ON places(region)
""")

cur.execute("""
CREATE INDEX IF NOT EXISTS idx_keyword
ON places(keyword)
""")

conn.commit()
conn.close()

print("DB 생성 완료!")