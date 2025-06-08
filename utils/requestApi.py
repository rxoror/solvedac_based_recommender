## api 호출 코드

import pandas as pd
import requests

## 사용자 부가정보 추출 함수
def get_user_info(handle):
    url = "https://solved.ac/api/v3/user/show"
    querystring = {"handle": handle}
    headers = {
        "x-solvedac-language": "ko",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    # 필요한 요소 추출, 없는 경우 None 처리
    user_data = {
        "handle": handle,
        "rating": data.get("rating"),
        "class": data.get("class"),
        "solvedCount": data.get("solvedCount"),
        "maxStreak": data.get("maxStreak")
    }

    # 1행짜리 DataFrame 반환
    return pd.DataFrame([user_data])


## 사용자 레이팅 수치 추출 함수
def get_user_rating(handle):
    url = "https://solved.ac/api/v3/user/show"
    querystring = {"handle": handle}
    headers = {
        "x-solvedac-language": "ko",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    data: dict = response.json()

    rating = data.get("rating")

    return rating # 해당 유저의 레이팅 수치를 반환함

# 문제의 번호를 받아서, 문제 제목을 반환
def get_problem_title(problem_num):
    url = "https://solved.ac/api/v3/problem/show"

    querystring = {"problemId":{problem_num}}

    headers = {
        "x-solvedac-language": "",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()
    data: dict = response.json()

    title = data.get("titleKo")

    return title
