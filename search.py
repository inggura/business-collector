import sqlite3

conn = sqlite3.connect("fortune.db")
cur = conn.cursor()

while True:

    keyword = input("\n검색어(종료=q) : ")

    if keyword.lower() == "q":
        break

    cur.execute("""
    SELECT
        name,
        phone,
        address,
        rating,
        reviews
    FROM places
    WHERE
        name LIKE ?
    ORDER BY reviews DESC
    """, (f"%{keyword}%",))

    rows = cur.fetchall()

    print(f"\n검색결과 : {len(rows)}개\n")

    for row in rows:

        print("=" * 60)
        print("이름 :", row[0])
        print("전화 :", row[1])
        print("주소 :", row[2])
        print("평점 :", row[3])
        print("리뷰 :", row[4])

conn.close()