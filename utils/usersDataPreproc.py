# 데이터 처리 코드

import pandas as pd

# ----------전역변수영역-----------
step_size = 10  # 단계 군집 별 유저 수 설정
# ------------------------------


# 전체 유저 데이터 전처리 (이상치제거, 정렬, 레이팅 순으로 step_size 만큼 묶기)
def get_filtered_ALL(): 
    df = pd.read_csv("data/solvedac_users.csv")

    ## solved.ac에서 일정 수준 이상의 활동을 한 유저만 분석 대상으로 포함 (이상치 제거)
    df = df[(df['solvedCount'] > 0) & (df['solvedCount'] < 10000)] # 0 < solvedCount < 10,000
    df = df[df['rating'] > 30] # 30 < rating
    df = df.sort_values(by='rating', ascending=True).reset_index(drop=True) # rating 오름차순 정렬

    ## 레이팅 순서대로 레벨을 생성 
    df['level'] = df.index // step_size # 레벨 컬럼 생성
    
    return df


# 비슷한 레이팅의 유저군 뽑아오기 (step_size 만큼)
def get_similar_users(rating_value):
    df = get_filtered_ALL()

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
    
