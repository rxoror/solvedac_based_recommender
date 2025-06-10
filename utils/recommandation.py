# 추천 함수 코드

import random
import json
import requests

TAG8 = ["math", "implementation", "greedy", "string", "data_structures", "graphs", "dp", "geometry"]
INTERNAL_COUNT = 5

def get_problem(user, performance, tag_performance):
    # 퍼포먼스 +- 2
    p1 = max(int(performance), 1)
    p2 = min(int(performance)+2, 30)
    # 태그는 편의상 랜덤으로 고름
    tag = random.choice(TAG8)
    url = f"https://solved.ac/api/v3/search/problem?query=*{p1}..{p2}+-s%40{user}+%23{tag}+solvable%3Atrue&sort=random&page=1"
    print(url)
    headers = {
        "x-solvedac-language": "ko",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    items = data.get("items")
    item = items[0]
    # 검색쿼리의 첫번째 문제
    # 골라진 태그랑 문제 번호 문제 타이틀
    return (tag, item["problemId"], item["titleKo"], item["level"])

def update_performance(rating, solved, performance_internal):
    # 못 푼 경우 퍼포먼스 공식에 사용되는 값은 0
    real_rating = rating if solved else 0
    # 내부 퍼포먼스에 포함된 레이팅값을 오래된 것을 제거
    performance_internal.append(real_rating)
    performance_internal.pop(0)

    return sum(performance_internal) / INTERNAL_COUNT

def update_tag_performance(tag, rating, solved, tag_performance_internal):
    # 못 푼 경우 퍼포먼스 공식에 사용되는 값은 0
    real_rating = rating if solved else 0
    performance_internal = tag_performance_internal[TAG8.index(tag)]
    # 내부 퍼포먼스에 포함된 레이팅값을 오래된 것을 제거
    performance_internal.append(real_rating)
    performance_internal.pop(0)

    return [sum(t) / INTERNAL_COUNT for t in tag_performance_internal]
