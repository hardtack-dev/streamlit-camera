# 메인 엔트리 포인트
import streamlit as st

# 페이지 환경설정
st.set_page_config(
    page_title="나에게 맞는 카메라는?",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 사이드바 숨김처리
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] { display: none !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# 세션 상태 초기화 
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user_name" not in st.session_state: st.session_state.user_name = ""
if "show_expire_warning" not in st.session_state: st.session_state.show_expire_warning = False #새로고침(F5) 시 세션 만료 경고 표시 여부

# 페이지 네비게이션 정의
pages = st.navigation([
    st.Page("pages/1_landing.py", title="시작하기", icon="🏠"),
    st.Page("pages/2_guide.py", title="가이드", icon="📋"),
    st.Page("pages/3_quiz.py", title="퀴즈", icon="📝"),
    st.Page("pages/4_result.py", title="결과", icon="🏆")
])

# 3. 앱 실행
pages.run()