## 유사 유저 분석 PAGE

import streamlit as st
import time
import pandas as pd
from utils import usersDataPreproc as udp
from utils import cosineSimilarity as cosSim

st.set_page_config(layout="wide", initial_sidebar_state="collapsed") #넓은 레이아웃, 사이드바 자동숨김

user_id = st.session_state.get("user_id", None) # 입력받은 값 받아오기
user_rating = udp.get_user_rating(user_id)

st.header("사용자 분석 PAGE")
st.subheader(f"'{user_id}'의 현재 rating : {user_rating}")

container_1 = st.container()
container_2 = st.container()
col_1, col_2, col_3, col_4   = st.columns(4)

#with container_1:

with container_2:
    if user_id:
        with col_1:
            st.write("아래는 비슷한 rating 수치의 집단 10명 입니다.")
            st.dataframe(udp.get_similar_users(user_rating))
            
        with col_2:
            st.write("정규화 된 데이터 (class, solvedCount, maxStreak)")
            new_df = udp.get_similar_users(user_rating)
            #user_info_df = udp.get_user_info(user_id)
            #new_df = pd.concat([new_df, user_info_df], ignore_index=True)
            
            st.dataframe(udp.normalize_df(new_df))
        with col_3:
            st.write("사용자의 기존 정보")
            st.dataframe(udp.get_user_info(user_id))


if st.button("메인 페이지로 돌아가기"):
    st.switch_page("main.py")
    user_id = 0

st.button("문제 추천 받기")