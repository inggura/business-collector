import sqlite3

print("=== 전국 점집 DB 프로젝트 ===")

conn = sqlite3.connect("fortune.db")

print("DB 연결 성공!")

conn.close()

print("프로그램 종료")