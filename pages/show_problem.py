import streamlit as st
from utils import makeFigure
from utils import requestApi as api
from utils import recommandation as rc
import random

st.set_page_config(layout="wide", initial_sidebar_state="collapsed") #넓은 레이아웃, 사이드바 자동숨김
user_id = st.session_state.get("user_id", None) # 유저 ID 불러오기




### >> 기능

def recommandation():   # 추천 문제를 불러와 session_state에 저장
    
    # p의 요소 : tag, item["problemId"], item["titleKo"], item["level"]
    p = rc.get_problem(user_id, st.session_state["performance"], st.session_state["tag_performance"]) # 문제 정보 저장
    
    # p의 요소를 재분배 >> session_state (전역 사용 가능)
    tag, pid, pname, level = p  
    st.session_state["current_tag"] = tag
    st.session_state["problem_number"] = pid
    st.session_state["problem_title"] = pname
    st.session_state["problem_level"] = level
    
    print(p)

def update_performance(solved): # 문제 풀이 결과에 따라 퍼포먼스 업데이트
    st.session_state["performance"] = \
        rc.update_performance(st.session_state["problem_level"], solved, st.session_state["performance_internal"])

    st.session_state["tag_performance"] = \
        rc.update_tag_performance(st.session_state["current_tag"],
                              st.session_state["problem_level"],
                              solved, st.session_state["tag_performance_internal"])

    print(st.session_state["tag_performance"])

recommandation() # 추천 문제를 불러와 session_state에 저장

### << 기능




### Front code area >>
st.title("추천 된 문제 보기")

container_1 = st.container()
container_2 = st.container()
container_3 = st.container()

col_L, col_R = st.columns(2)

col_1, col_2 = st.columns(2)

with col_L:
    st.subheader(f"{user_id} 의 활동 현황")

    st.write("사용자 부가 정보")
    st.dataframe(api.get_user_info(user_id))
    
    st.write("현재 난이도")
    st.subheader(f"`{st.session_state['performance']}`")

    st.write("사용자의 카테고리별 성과")
    st.plotly_chart(makeFigure.make_figure(st.session_state["tag_performance"]))

with col_R:
    
    #matrix = f'''
    ###### "{user_id}" 님의 문제 플이 기반 추천은 다음과 같습니다. 
    #|문제 번호|문제 이름|바로가기|
    #|:------:|:------:|:------:|
    #|{st.session_state["problem_number"]}|{st.session_state["problem_title"]}|[문제 페이지로 이동](https://www.acmicpc.net/problem/{st.session_state["problem_number"]})|
    #'''
    
    st.subheader("추천 문제")
    if st.session_state["is_random_tag"] == True:
        st.badge(f"Random 적용됨", icon=":material/ifl:", color="violet")
    st.badge(f"{st.session_state["current_tag"]}", icon=":material/tag:", color="primary")

    st.link_button(f"{st.session_state["problem_number"]}번 / 문제 제목 : {st.session_state["problem_title"]} (클릭 시 이동)", f"https://www.acmicpc.net/problem/{st.session_state["problem_number"]}", type = "tertiary", use_container_width=False)

    st.write("") # 빈 줄
    st.write("")
    
    # 성공 여부 버튼
    if st.button("풀기에 성공했어요", type = "primary", icon=":material/check_circle:", use_container_width=True) :
        update_performance(True)
        #st.switch_page("./pages/show_problem.py")

    if st.button("풀지 못했어요", icon=":material/disabled_by_default:", type = "tertiary", use_container_width=True):
        update_performance(False)
        #st.switch_page("./pages/show_problem.py")

    st.divider() # 구분선

    if st.button("카테고리 다시 선택", type = "tertiary", icon=":material/arrow_back_ios:", use_container_width=True):
        st.switch_page("pages/show_similar.py")

    if st.button("메인으로 돌아가기", type = "tertiary", icon=":material/home:", use_container_width=True):
        st.switch_page("main.py")

### << Front code area


### 메모 (태호윤 작성)
#
# 원래는 페이지 내에 백준사이트를 임베드 하고자함.
# 페이지를 임베드 시 백준 사이트 정책상 차단되는 문제가 있음.
# 따라서 마크다운 형식을 통해 바로가기 링크를 만드는거로 우회함.
#  
# 6/11
# main, show_similar, show_problem 페이지 ui 개선
# 코드 가시성 개선
# 