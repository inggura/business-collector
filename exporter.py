import sqlite3
import pandas as pd

conn = sqlite3.connect("fortune.db")

df = pd.read_sql_query("SELECT * FROM places", conn)

df.to_csv(
    "fortune_places.csv",
    index=False,
    encoding="utf-8-sig"
)

print("CSV 저장 완료")

conn.close()