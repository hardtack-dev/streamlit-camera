# pages/1_landing.py (시작&로그인 페이지)
import streamlit as st
from core import toolbox as tb  # core 폴더의 toolbox를 tb라는 이름으로 임포트

# 세션 확인 (로그인 여부)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 세션 만료 경고 (새로고침용)
if st.session_state.get("show_expire_warning", False):
    st.toast("세션이 만료되었습니다. 다시 로그인해 주세요.", icon="🚨")
    st.session_state.show_expire_warning = False


# 로그인 다이얼로그 함수
@st.dialog("로그인")
def login_dialog():
    user_id = st.text_input("아이디를 입력하세요")
    user_pw = st.text_input("비밀번호를 입력하세요", type="password")
    
    if st.button("접속 및 시작!", width="stretch", type="primary"):
        # 도구함의 데이터 로더 사용
        user_db = tb.load_json_data("users.json")
        
        # 자료형 오류 방지를 위해 str()로 통일하여 비교
        if user_id in user_db and str(user_db[user_id]) == str(user_pw):
            st.session_state.logged_in = True
            st.session_state.user_name = user_id
            st.switch_page("pages/2_guide.py")
        else:
            st.error("정보가 없거나, 아이디 또는 비밀번호가 일치하지 않습니다.")


# 메인 레이아웃 구성 (1 : 2 : 1)
_, main_content, _ = st.columns([1, 2, 1])

with main_content:
    _, img_center, _ = st.columns([1, 2, 1])
    with img_center:
        st.image("images/landing/main.png")
    
    st.markdown("<h2 style='text-align: center;'> 여러분에게 맞는 카메라를 추천해드립니다!</h2>", unsafe_allow_html=True)
    st.write("---")
    
    # 좌우 레이아웃 구성 (6 : 4)
    desc_col, info_col = st.columns([0.6, 0.4])

    with desc_col:
        with st.container(border=True, height=215):
            st.subheader("무슨 테스트 인가요?")
            st.write("""
            수많은 카메라 기종과 렌즈, 어려운 용어들.... \n\n **무엇을 선택해야 할 지 막막하신가요?**
            사용자의 습관과 취향을 분석하여, 여러분에게 맞는 성격의 카메라를 제안해 드립니다.
            """)   

    with info_col:
        with st.container(border=True):
            st.markdown(":violet-badge[:material/star: 오픈소스소프트웨어 실습] :orange-badge[중간고사 대체과제]")
        with st.container(border=True):    
            st.markdown("##### ✨ 제출자")
            st.markdown("###### **학번:** 2023204006")
            st.markdown("###### **이름:** 하건우")

    # 로그인/테스트 시작
    if st.button("로그인하여 테스트 시작하기", type="primary", width="stretch"):
        if st.session_state.logged_in:
            st.switch_page("pages/2_guide.py")
        else:
            login_dialog()