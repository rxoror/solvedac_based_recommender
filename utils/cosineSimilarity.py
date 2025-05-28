# 유사 집단과 서비스 사용자의 Cosine Sinilarity 를 계산

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def get_cosine_similarities(df, target_handle):
    df = df.reset_index(drop=True)
    if target_handle not in df['handle'].values:
        raise ValueError(f"Handle '{target_handle}' not found in DataFrame.")

    # 코사인 유사도 계산 대상 컬럼
    feature_cols = ["class", "solvedCount", "maxStreak"]
    features = df[feature_cols]

    # 기준 유저 벡터 추출
    target_index = df[df['handle'] == target_handle].index[0]
    target_vector = features.iloc[[target_index]]

    # 유사도 계산
    similarities = cosine_similarity(features, target_vector).flatten()

    return df.assign(cosine_similarity=similarities).drop(index=target_index).reset_index(drop=True)
