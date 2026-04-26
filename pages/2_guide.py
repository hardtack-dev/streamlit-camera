# pages/2_guide.py (가이딩 페이지)
import streamlit as st
from core import toolbox as tb

# 로그인 여부 체크 (미 로그인시, landing페이지로 )
tb.check_login()

# 퀴즈 질문/결과 데이터 미리 캐싱
# 결과 이미지 파일 미리 캐싱
quiz_data = tb.load_json_data_cached("questions.json")
result_data = tb.load_json_data_cached("result.json")
tb.preload_all_camera_images(result_data)

# 세션에서 사용자 이름 가져오기
user_name = st.session_state.get("user_name", "사용자")


# 메인 레이아웃 구성 (1 : 2 : 1)
left_space, main_content, right_space = st.columns([1, 2, 1])

with main_content:
    st.title(f"📋 반가워요, {user_name}님!")
    st.write("---")
    
    # 퀴즈 안내 영역
    with st.container():
        guide_col, warning_col = st.columns([1, 1])

        with guide_col:
            with st.container(border=True):
                st.subheader("💡 퀴즈는 이렇게 진행돼요")
                st.markdown("""
                1. **문항 구성**: 총 15개의 객관식 질문
                2. **분석 방식**: 선택하신 답변을 바탕으로 최적의 카메라를 매칭합니다.
                3. **진행 시간**: 약 5분 내외 소요
                """)

        with warning_col:
            with st.container(border=True):
                st.subheader("⚠️ 주의사항")
                st.warning("""
                - 모든 문항에 답변해야 결과가 나와요.
                - 고민되는 질문이 있다면 가볍게 선택하고 넘어가세요!
                """)

        st.write("\n\n")

        # 퀴즈 시작 버튼
        if st.button("🚀 테스트 시작하기", type="primary", width="stretch"):
            st.switch_page("pages/3_quiz.py")
        
        # 로그아웃 버튼
        if st.button("로그아웃 하기", width="stretch"):
            tb.show_logout_dialog()