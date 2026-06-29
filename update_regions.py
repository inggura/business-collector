print("★★★★ update_regions.py 실행됨 ★★★★")

import pandas as pd

regions = [
    "서울 강남구",
    "서울 서초구",
    "서울 송파구",
    "서울 강동구",
    "서울 종로구",
    "서울 중구",
    "서울 용산구",
    "서울 성동구",
    "서울 광진구",
    "서울 동대문구"
]

df = pd.DataFrame(regions, columns=["region"])

df.to_csv(
    "data/regions_all.csv",
    index=False,
    encoding="utf-8-sig"
)

print("생성 완료!")
print(df)