import streamlit as st
from core import toolbox as tb

# 로그인 여부 체크 (미 로그인시, landing페이지로 )
tb.check_login()

quiz_data = tb.load_json_data_cached("questions.json")


# 퀴즈 수행 중, 나갈 시
@st.dialog("잠시만요!")
def quizout_dialog():
    st.caption("지금 나가면 결과가 초기화돼요. 정말로 시작페이지로 이동할까요? ")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("네, 그만둘래요", type="primary", width="stretch"):
            st.session_state.answers = {}
            st.session_state.current_q = 0
            st.switch_page("pages/2_guide.py")
    with col2:
        if st.button("취소", width="stretch", type="secondary"):
            st.rerun()

#  segmented control의 버튼 활성화 감지
def handle_nav_change():
    if st.session_state.get("return_guide") == "🏠 시작 화면으로 돌아가기":
        st.session_state.return_guide = None
        st.session_state.trigger_dialog = True

# 퀴즈 버튼 높이 조절용 CSS 
st.markdown("""
            <style>  
                div.stButton > button { height: 100px !important }; 
            </style> """, 
    unsafe_allow_html=True)

# 질문 데이터 로딩
# 미리 캐싱된 데이터 가져오기 (toolbox의 캐싱 로더 활용)


if "current_q" not in st.session_state: st.session_state.current_q = 0
if "answers" not in st.session_state: st.session_state.answers = {}

# 메인 레이아웃 구성 (1 : 2 : 1)
# col1과 col3는 좌우 여백용, col2가 컨텐츠 영역
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # 현재 질문 인덱스 번호
    curr_idx = st.session_state.current_q

    # 시작화면으로 돌아가기 버튼
    nav_options = ["🏠 시작 화면으로 돌아가기"]
    st.segmented_control("메뉴", nav_options, selection_mode="single", 
                         label_visibility="collapsed", key="return_guide", on_change=handle_nav_change)

    # 로그아웃 여부 다이얼로그 트리거 여부 확인
    if st.session_state.get("trigger_dialog", False):
        st.session_state.trigger_dialog = False
        quizout_dialog()
    
    # 진행률 표시
    progress = (curr_idx + 1) / len(quiz_data) # (현재 질문의 인덱스 번호 / 받아온 질문 데이터의 길이) 하여 진행률 계산
    st.progress(progress)
    
    # 진행률에 따른 st.badge의 위치조절
    progress_ratio = max(0.05, progress - 0.01)
    spacer_ratio = max(0.05, 1.0 - progress - 0.05)
    col_prog, col_badge, col_rest = st.columns([progress_ratio, 0.2, spacer_ratio])

    # 퀴즈 남은 갯수 렌더링
    with col_badge:
        if progress < 1.0:
            st.badge(f"{len(quiz_data) - (curr_idx + 1)}개 남음", color="green")
        else:
            st.badge("마지막 질문이에요!", color="blue")
    
    # 퀴즈 데이터에서 질문 렌더링
    # 퀴즈 데이터[인덱스 번호][질문]으로 접근
    st.markdown(f"<h2 style='text-align: center;'> {quiz_data[curr_idx]['question']}</h2>", unsafe_allow_html=True) # native 마크다운 문법의 한계로, html 렌더링
    st.write("---")

    # 퀴즈 데이터 옵션 렌더링
    options = quiz_data[curr_idx]["options"] # [인덱스 번호][options 배열]으로 접근하여, 버튼으로 렌더링
    for i in range(0, len(options), 2): # 2개 열로 렌더링하기 위해, 2개씩 묶어서 처리 i=2씩 증가
        row_options = options[i:i+2]    # 선택지를 2씩 묶어주기 [a,b], [c,d] 형태로 묶어서 처리
        cols = st.columns(2)            # 2개 열로 컬럼 생성
        for j, opt in enumerate(row_options): # 각 열에 대해, j:0,1(인덱스) / opt:실제 옵션 데이터
            btn_idx = i + j                   # 실제 옵션의 인덱스 번호 계산 (i는 0,2,4... / j는 0,1이므로, btn_idx는 0,1,2,3...)
            if cols[j].button(opt["text"], key=f"btn-{btn_idx}", width="stretch"): # 각 열의 버튼 렌더링, 클릭 시 btn_idx로 어떤 옵션이 선택됐는지 알 수 있음 
                st.session_state.answers[curr_idx] = btn_idx # 대답에는 질문 인덱스 번호와, 선택한 옵션의 인덱스 번호 저장
                if curr_idx < len(quiz_data) - 1:   # 마지막 질문이 아니라면, 다음 질문으로 이동
                    st.session_state.current_q += 1 # 다음 질문으로 이동하기 위해, current_q 인덱스 번호 1 증가
                    st.rerun()  # 페이지 다시 렌더링
                else:
                    st.switch_page("pages/4_result.py") # 마지막 질문이라면, 결과 페이지로 이동

    st.write("---")
    
    nav_col1, nav_col_spacer, nav_col2 = st.columns([1, 4, 1], gap="medium")
    with nav_col1:
        if curr_idx > 0:
            if st.button("⬅️ 이전", key="btn_prev", type="tertiary", width="stretch"):
                st.session_state.current_q -= 1
                st.rerun()
            
    with nav_col2:
        if curr_idx in st.session_state.answers and curr_idx < len(quiz_data) - 1:
            if st.button("다음 ➡️", key="btn_next", type="tertiary", width="stretch"):
                st.session_state.current_q += 1
                st.rerun()