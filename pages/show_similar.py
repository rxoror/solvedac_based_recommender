## PAGE : 유사 유저 분석

import streamlit as st
from utils import usersDataPreproc as udp
from utils import requestApi as api

st.set_page_config(layout="wide", initial_sidebar_state="collapsed") #넓은 레이아웃, 사이드바 자동숨김

# 페이지 간 변수 전달 "session_state" 사용
user_id = st.session_state.get("user_id", None) # 입력받은 값 받아오기
user_rating = api.get_user_rating(user_id)

st.title("문제 카테고리 선택")
st.subheader(f"'{user_id}'의 현재 rating : {user_rating}")

container_1 = st.container()
container_2 = st.container()
col_1, col_2 = st.columns(2)

with container_1:
    if user_id:
        #st.write("사용자의 기존 정보")
        st.dataframe(api.get_user_info(user_id))
        
        #st.write("비슷한 rating 수치의 사용자 10명 입니다.")
        #st.write("아래 사용자들이 푼 문제를 분석하여 추천 해드릴게요!")
        #st.dataframe(udp.get_similar_users(user_rating))
                  
    
st.session_state["is_random_tag"] = True ## 미선택 시 랜덤 (기본 값)
#print(f"Your selected options: {st.session_state["current_tag"]}.")


# 태그 선택 기능 (미선택 시 랜덤)
options = ["math", "implementation", "greedy", "string", "data_structures", "graphs", "dp", "geometry"]
selection = st.pills("문제 카테고리를 직접 선택할 수도 있어요.", options, selection_mode="single")



if selection: ## Tag 선택 시 session_state 에 저장
    st.session_state["is_random_tag"] = False
    st.session_state["current_tag"] = selection
    st.badge(f"{st.session_state["current_tag"]}", icon=":material/tag:", color="primary")
    #st.markdown(f"Your selected options: {st.session_state["current_tag"]}.")
    #print(f"Your selected options (update): {st.session_state["current_tag"]}.")
else:
    st.session_state["is_random_tag"] = True
    st.badge(f"Random", icon=":material/ifl:", color="violet")




## '문제 추천 받기' 버튼
if st.button("문제 추천 받기", type = "primary", icon=":material/check_circle:", use_container_width=True):
    
    st.session_state["performance"] = 12
    
    #퍼포먼스 변경 공식을 위함
    st.session_state["performance_internal"] = [12] * 5
    st.session_state["tag_performance"] = [1, 2, 3, 4, 5, 6, 7, 8]
    
    # 태그 퍼포먼스 변경 공식을 위함
    st.session_state["tag_performance_internal"] = [[i+1] * 5 for i in range(8)]

    # 테스트용 코드
    #st.session_state["user_id"] = "your0501"
    #st.session_state["problem_number"] = 1000
    #st.session_state["current_tag"] = "math" ## Tag
    #st.session_state["problem_title"] = "A+B"
    #st.session_state["problem_level"] = 1
    
    st.switch_page("pages/show_problem.py")













st.divider()

if st.button("메인으로 돌아가기", type = "tertiary", icon=":material/home:", use_container_width=True):
    st.switch_page("main.py")
    user_id = 0