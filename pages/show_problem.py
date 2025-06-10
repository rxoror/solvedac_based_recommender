import streamlit as st
from utils import makeFigure
from utils import requestApi as api
from utils import recommandation as rc
import random

st.set_page_config(layout="wide", initial_sidebar_state="collapsed") #넓은 레이아웃, 사이드바 자동숨김

st.title("추천 된 문제 보기")

col_1, col_2 = st.columns(2)

with col_1:
    st.subheader("현재 난이도")
    st.subheader(f"`{st.session_state['performance']}`")
with col_2:
    st.subheader("태그별 퍼포먼스")
    st.plotly_chart(makeFigure.make_figure(st.session_state["tag_performance"]))

st.divider()

### 문제 추천 확정 함수에서 아래 코드 적용 (빈칸에는 전달 할 문제 번호 대입) ###
# st.session_state["problem_number"] = ____

user_id = st.session_state.get("user_id", None) # 유저 ID 불러오기

#problem_number = st.session_state.get("problem_number", None) # 문제 번호 불러오기
#problem_title = api.get_problem_title(problem_number) # 문제 제목 불러오기

def recommandation():
    p = rc.get_problem(user_id, st.session_state["performance"], st.session_state["tag_performance"])
    tag, pid, pname, level = p
    st.session_state["current_tag"] = tag
    st.session_state["problem_number"] = pid
    st.session_state["problem_title"] = pname
    st.session_state["problem_level"] = level
    print(p)

def update_performance(solved):
    st.session_state["performance"] = \
        rc.update_performance(st.session_state["problem_level"], solved, st.session_state["performance_internal"])

    st.session_state["tag_performance"] = \
        rc.update_tag_performance(st.session_state["current_tag"],
                              st.session_state["problem_level"],
                              solved, st.session_state["tag_performance_internal"])

    print(st.session_state["tag_performance"])

recommandation()

matrix = f'''
    ###### "{user_id}" 님의 문제 플이 기반 추천은 다음과 같습니다. 
    |문제 번호|문제 이름|바로가기|
    |:------:|:------:|:------:|
    |{st.session_state["problem_number"]}|{st.session_state["problem_title"]}|[문제 페이지로 이동](https://www.acmicpc.net/problem/{st.session_state["problem_number"]})|
'''

st.markdown(matrix)

if st.button("Solve!!"):
    update_performance(True)
    #st.switch_page("./pages/show_problem.py")

if st.button("포기"):
    update_performance(False)
    #st.switch_page("./pages/show_problem.py")

if st.button("메인으로 돌아가기"):
    st.switch_page("main.py")



### 메모 (태호윤 작성)
#
# 원래는 페이지 내에 백준사이트를 임베드 하고자함.
# 페이지를 임베드 시 백준 사이트 정책상 차단되는 문제가 있음.
# 따라서 마크다운 형식을 통해 바로가기 링크를 만드는거로 우회함.
#  