import sqlite3

conn = sqlite3.connect("fortune.db")
cur = conn.cursor()

# 전체 업체 수
cur.execute("SELECT COUNT(*) FROM places")
total = cur.fetchone()[0]

print("=" * 40)
print(f"총 업체 수 : {total}")
print("=" * 40)

# 지역별 개수
cur.execute("""
SELECT region, COUNT(*)
FROM places
GROUP BY region
ORDER BY COUNT(*) DESC
""")

print("\n지역별 현황")

for region, cnt in cur.fetchall():
    print(f"{region:10} {cnt}개")

conn.close()