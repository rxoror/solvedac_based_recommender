## PAGE : 유사 유저 분석

import streamlit as st
from utils import usersDataPreproc as udp
from utils import requestApi as api

st.set_page_config(layout="wide", initial_sidebar_state="collapsed") #넓은 레이아웃, 사이드바 자동숨김

# 페이지 간 변수 전달 "session_state" 사용
user_id = st.session_state.get("user_id", None) # 입력받은 값 받아오기
user_rating = api.get_user_rating(user_id)

st.header("사용자 분석 PAGE")
st.subheader(f"'{user_id}'의 현재 rating : {user_rating}")

container_1 = st.container()
container_2 = st.container()
col_1, col_2 = st.columns(2)

#with container_1:

with container_2:
    if user_id:
        st.write("사용자의 기존 정보")
        st.dataframe(api.get_user_info(user_id))
        
        with col_1:
            st.write("아래는 비슷한 rating 수치의 집단 10명 입니다.")
            st.dataframe(udp.get_similar_users(user_rating))
            
        with col_2:
            st.write("정규화 된 데이터 (class, solvedCount, maxStreak)")
            new_df = udp.get_similar_users(user_rating)
            #user_info_df = udp.get_user_info(user_id)
            #new_df = pd.concat([new_df, user_info_df], ignore_index=True)
            
            st.dataframe(udp.normalize_df(new_df))        
    

if st.button("메인 페이지로 돌아가기"):
    st.switch_page("main.py")
    user_id = 0

if st.button("문제 추천 받기"):
    # 이 줄에 문제 번호 확정코드를 넣으면 됩니다.
    # 예시 : 
    # recomm_num = ___(user_id)
    # st.session_state["problem_number"] = recomm_num # 페이지 간 변수 전달 (전역변수와 유사)
    # st.session_state["problem_number"] = 1000 # 이 줄의 코드는 테스트 코드입니다.
    
    st.session_state["performance"] = 12
    #퍼포먼스 변경 공식을 위함
    st.session_state["performance_internal"] = [12] * 5
    st.session_state["tag_performance"] = [1, 2, 3, 4, 5, 6, 7, 8]
    # 태그 퍼포먼스 변경 공식을 위함
    st.session_state["tag_performance_internal"] = [[i+1] * 5 for i in range(8)]

    # 테스트용 코드
    st.session_state["user_id"] = "your0501"
    st.session_state["problem_number"] = 1000
    st.session_state["current_tag"] = "math"
    st.session_state["problem_title"] = "A+B"
    st.session_state["problem_level"] = 1
    
    st.switch_page("pages/show_problem.py")