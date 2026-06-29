import sqlite3
import pandas as pd

conn = sqlite3.connect("fortune.db")

df = pd.read_sql_query("""
SELECT
    name,
    phone,
    address,
    rating,
    reviews,
    website,
    business_status
FROM places
ORDER BY name
""", conn)

conn.close()

df.to_excel("fortune.xlsx", index=False)

print(f"엑셀 저장 완료! ({len(df)}개)")