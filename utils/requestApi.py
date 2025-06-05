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

def get_user_solvedcount(handle):
    url = "https://solved.ac/api/v3/user/show"
    querystring = {"handle": handle}
    headers = {
        "x-solvedac-language": "ko",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    data: dict = response.json()
    
    solvedcount = data.get("solvedCount")

    return solvedcount

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

## 두 사용자가 모두 푼 문제의 개수
def compare_user_problem(handle, handle2):
    url = f"https://solved.ac/api/v3/search/problem?query=solved_by:{handle}%20solved_by:{handle2}&page=1"
    print(url)
    querystring = {"handle": handle}
    headers = {
        "x-solvedac-language": "ko",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    count = data.get("count")
    return count