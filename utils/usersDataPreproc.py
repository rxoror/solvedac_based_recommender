# 데이터 처리 코드

import pandas as pd
from utils import requestApi as api

# ----------전역변수영역-----------

step_size = 10  # 단계 군집 별 유저 수 설정

# ------------------------------


# 전체 유저 데이터 전처리 (이상치제거, 정렬, 레이팅 순으로 step_size 만큼 묶기)
df = pd.read_csv("data/solvedac_users.csv")

## solved.ac에서 일정 수준 이상의 활동을 한 유저만 분석 대상으로 포함 (이상치 제거)
df = df[(df['solvedCount'] > 0) & (df['solvedCount'] < 10000)] # 0 < solvedCount < 10,000
df = df[df['rating'] > 30] # 30 < rating
df = df.sort_values(by='rating', ascending=True).reset_index(drop=True) # rating 오름차순 정렬

## 레이팅 순서대로 레벨을 생성 
df['level'] = df.index // step_size # 레벨 컬럼 생성



# 비슷한 레이팅의 유저군 뽑아오기 (step_size 만큼)
def get_similar_users(rating_value):
    #df = get_filtered_ALL()

    match = df[df['rating'] >= rating_value]
    if match.empty:
        idx = len(df) - 1
    else:
        idx = match.index[0]
    
    level = idx // step_size

    return df[df['level'] == level] # 'step_size' 'n'명의 유사군집 반환


# 유자 집단 데이터 프레임 정규화
def normalize_df(df):
    cols_to_normalize = ["class", "solvedCount", "maxStreak"]
    df_norm = df.copy()
    for col in cols_to_normalize:
        min_val = df_norm[col].min()
        max_val = df_norm[col].max()
        if max_val - min_val == 0:
            df_norm[col] = 0.0
        else:
            df_norm[col] = (df_norm[col] - min_val) / (max_val - min_val)
    return df_norm

 
### 
# diceCoefficient 기반 유사도 계산 #
# solved 검색 쿼리를 이용 (두 사용자가 풀었던 겹친 문제의 개수를 기반으로 계산함)

def get_similar_users_problem(rating_value, handle, solvedCount):
    #df = get_filtered_ALL()

    # rating 기준으로 정렬된 상태에서 해당 인덱스 찾기
    idx = df[df['rating'] >= rating_value].index.min()
    if pd.isna(idx):  # rating이 가장 높은 경우
        idx = len(df) - 1
    level = idx // step_size
    
    data = df[df['level'] == level].copy()

    #del data['tier']
    del data['class']
    del data['solvedCount']
    del data['level']

    #data['solvedCount'] = data.apply(lambda x: x["handle"], axis=1)
    data['solvedCount'] = data.apply(lambda x: getsolvedcount(x["handle"]), axis=1)
    data['intersection'] = data.apply(lambda x: getIntersect(handle, x["handle"]), axis=1)
    data['diceCoefficient'] = 2 / (data['solvedCount'] + solvedCount) * data['intersection']

    return data # 'step_size' 'n'명의 유사군집 반환

def getsolvedcount(handle2):
    return api.compare_user_problem(handle2, handle2)

def getIntersect(handle1, handle2):
    return api.compare_user_problem(handle1, handle2)

# diceCoefficient 기반 유사도 계산 #
# 코드 개발 : 최윤혁 #
###