# 전체 유저 데이터를 업데이트

import requests
import csv
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# 유저 랭킹 리스트 가져오기 (멀티스레딩 + 자동 저장)
def get_many_users_by_tier(max_pages=4000, save_interval=100, save_path="data/solvedac_users.csv"):
    url = "https://solved.ac/api/v3/ranking/tier"
    headers = {"User-Agent": "Mozilla/5.0"}

    def fetch_page(page):
        try:
            response = requests.get(url, headers=headers, params={"page": page}, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get("items", [])
            else:
                print(f"❌ 요청 실패 (페이지 {page}):", response.status_code)
                return []
        except requests.RequestException as e:
            print(f"❌ 예외 발생 (페이지 {page}): {e}")
            return []

    all_users = []
    os.makedirs(os.path.dirname(save_path), exist_ok=True)  # 디렉토리 없으면 생성

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(fetch_page, page): page for page in range(1, max_pages + 1)}
        for count, future in enumerate(as_completed(futures), 1):
            result = future.result()
            if result:
                all_users.extend(result)
                print(f"📦 {len(all_users)}명 수집됨")

            # 자동 저장 (예: 100페이지마다)
            if count % save_interval == 0:
                save_users_to_csv(all_users, filename=save_path)
                print(f"💾 중간 저장됨 ({count} 페이지까지)")

    return all_users

# CSV로 저장
def save_users_to_csv(users, filename="data/solvedac_users.csv"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    fields = ["handle", "rating", "class", "solvedCount", "maxStreak"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for user in users:
            writer.writerow({field: user.get(field, "") for field in fields})
    print(f"✅ 저장 완료: {filename}")

# 실행
if __name__ == "__main__":
    users = get_many_users_by_tier(max_pages=4000, save_interval=100, save_path="data/solvedac_users.csv")
    save_users_to_csv(users, filename="data/solvedac_users.csv")