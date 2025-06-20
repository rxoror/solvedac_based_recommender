## PAGE : MAIN

import streamlit as st
import time

st.set_page_config(layout="wide", initial_sidebar_state="collapsed") #넓은 레이아웃, 사이드바 자동숨김

st.title('solved.ac 기반 맞춤 문제 추천')

col_L, col_R = st.columns(2)
with col_L:       # 사용자 ID 입력부

        user_input = st.text_input("사용자 ID를 입력하세요")
        if st.button("검색", type = "primary", icon=":material/search:", use_container_width=True):
                with st.spinner("데이터를 불러오는 중...", show_time=True): # 로딩 안내
                        time.sleep(2)
                if user_input :
                        st.session_state["user_id"] = user_input # 페이지 간 변수 전달 "session_state" 사용
                        st.switch_page("pages/show_similar.py")
                else:
                        st.badge("사용자 ID 를 입력하세요.", icon=":material/account_circle:", color="red")


with col_R:
        multi = '''

        ###### \'solved.ac\' 의 Api 기반으로 작동합니다. 따라서 사용자의 활동 정보를 활용합니다.

                본 프로젝트는 2025 '딥러닝프로젝트_어드벤처디자인' 의 8조가 제작하였습니다. 
                
        '''
        st.markdown(multi)
