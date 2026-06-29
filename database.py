import sqlite3

conn = sqlite3.connect("fortune.db")
cur = conn.cursor()

cur.execute("""
CREATE INDEX IF NOT EXISTS idx_region
ON places(region)
""")

cur.execute("""
CREATE INDEX IF NOT EXISTS idx_keyword
ON places(keyword)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS places(
    place_id TEXT PRIMARY KEY,
    name TEXT,
    address TEXT,
    latitude REAL,
    longitude REAL,
    rating REAL,
    reviews INTEGER,
    keyword TEXT,
    region TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()