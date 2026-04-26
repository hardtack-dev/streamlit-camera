import time
import plotly.express as px
import streamlit as st
import pandas as pd
import re
from core import toolbox as tb 

# 로그인 여부 체크 (미 로그인시, landing페이지로 )
tb.check_login()

quiz_data = tb.load_json_data_cached("questions.json")
result_data = tb.load_json_data_cached("result.json")


# 2, 3위 카메라 다이얼로그
@st.dialog("🔥 박빙의 승부! 다른 추천 카메라")
def show_competitors_dialog(competitors_list, result_data):
    st.markdown(f"1위와 점수 차이가 10점 미만인, {st.session_state.user_name}님과 아주 잘 맞는 또 다른 카메라들입니다.")
    table_data = []
    for rank, cam_key, score, diff in competitors_list:
        cam_info = result_data[0][cam_key]
        table_data.append({
            "순위": f"{rank}위",
            "모델명": cam_info["title"],
            "점수": f"{score}점 (1위와 {diff}점 차이)",
            "특징": cam_info["desc"].split('.')[0] + "."
        })
    df_competitors = pd.DataFrame(table_data)
    st.table(df_competitors.set_index("순위"))
    if st.button("확인 완료", width="stretch"):
        st.rerun()


#  점수 및 순위 계산 로직 
total_scores = {}                                               # 카테고리별 점수를 담을 딕셔너리
if "answers" in st.session_state:                               # 사용자가 푼 답변이 세션에 존재하는지 확인
    for q_idx, opt_idx in st.session_state.answers.items():     # 선택한 문항의 인덱스(q_idx)와 옵션의 인덱스(opt_idx)을 꺼내서 처리 
        scores = quiz_data[q_idx]["options"][opt_idx]["scores"] # JSON파일의 형식에 따라, q_idx(질문)에 따른 options(리스트), opt_idx(나의 답변)에 따른 socre(가중치 점수) 추출
        for category, value in scores.items():                  # 카테고리와 점수(가중치)를 순회
            total_scores[category] = total_scores.get(category, 0) + value # 카테고리별로 점수를 누적하여 계산, 키(카테고리)를 찾아 기존 점수에 현재 가중치 점수를 더하는 방식으로 총점 계산

close_competitors = []

# 결과 정렬 및 1위 값 추출
if total_scores:
    sorted_scores = sorted(total_scores.items(), key=lambda item: item[1], reverse=True) # total_scores 딕셔너리를 카테고리, 점수 기준으로 내림차순 정렬하여 저장
    best_camera_key = sorted_scores[0][0]                                   # 1위인 카메라의 키(카테고리명)를 추출
    best_score = sorted_scores[0][1]                                        # 1위인 카메라의 점수를 추출 (비교용)        
    result = result_data[0][best_camera_key]                                # 결과변수에 1위 카메라의 키를 찾아 상세 정보(이미지, 설명 등)를 저장
    formatted_desc = re.sub(r'([.!?])\s+', r'\1  \n\n', result["desc"])     # 설명 텍스트를 문장 단위로 나누는 로직(regex)
    
    # 2, 3위 결과 추출
    for rank in range(1, min(3, len(sorted_scores))):                       # 2위(idx 1)와 3위(idx 2)까지만 추출하도록 범위 설정
        cam_key = sorted_scores[rank][0]                                    # 순위별 카메라 키 추출
        score = sorted_scores[rank][1]                                      # 순위별 카메라 점수 추출  
        diff = best_score - score                                           # 1위(best_score)와의 점수 차이 계산         
                                                                            
        if diff < 10:                                                       # 1위와 점수 차이가 10점 미만인 경우에            
            close_competitors.append((rank + 1, cam_key, score, diff))      # 경쟁 카메라 리스트(close_competitors)에 추가
else:
    st.error("퀴즈를 완료하지 않으셨거나, 잘못된 접근입니다.")                       # 잘못된 접근일시 차단
    st.markdown("### 2초 뒤, 시작화면으로 이동합니다 ")
    time.sleep(2)
    st.switch_page("pages/1_landing.py")

# 메인 레이아웃 구성 (1 : 3 : 1)
left_space, main, right_space = st.columns([1, 3, 1])
with main:
       
    st.balloons()
    
    st.markdown(f"<h2 style='text-align: center;'> {st.session_state.user_name}님에게 맞는 카메라를 찾았어요!</h2>", unsafe_allow_html=True)
    st.write("---")

    left_recommend, right_spec = st.columns([1, 1])
    # 좌측 레이아웃
    with left_recommend:
        # 추천결과 화면
        image_path =  result["image_url"]
        img_bytes = tb.get_image_bytes(image_path)

        with st.container(border=True, height=580):
            
            if img_bytes is not None:
                st.image(img_bytes, width="stretch")
            else:
                st.error(f"이미지를 불러올 수 없습니다.")

            st.success(result["title"], icon="✅")
            st.markdown(f"###### {formatted_desc}")
        
        if st.button("다시 테스트하기", width="stretch", type="primary"):
            st.session_state.update({"current_q": 0, "answers": {}, "result_analyzed": False})
            st.switch_page("pages/2_guide.py")

        if st.button("로그아웃 하기", width="stretch"):
            tb.show_logout_dialog()
    
    # 우측 레이아웃
    with right_spec:
        with st.container(border=True, height=635):
            # 탭 3개 생성 (데이터 분석 결과, 카메라 세부 스펙, 나의 답변)
            tab_chart, tab_specs, tab_answers = st.tabs(["📊 데이터 분석 결과", "📸 추천 카메라 세부스펙", "✍️ 나의 답변"])

            # 탭1: 레이더 차트로 분석 결과 시각화
            with tab_chart:
                st.markdown("#### 📈 나의 카메라 취향 분석")
                if total_scores:
                    display_names = { # 카테고리 키를 사용자 친화적인 이름으로 매핑
                        "Sony_Hybrid": "⚖️ 소니 하이브리드", "Sony_Video": "🎥 소니 브이로그",
                        "Canon_Photo": "📸 캐논 프로(사진)", "Sony_Photo": "🖼️ 소니 고해상도",
                        "Canon_Hybrid": "🏃 캐논 경량풀프", "Canon_Crop": "🎒 캐논 입문용",
                        "Nikon_Photo": "🕰️ 니콘 레트로", "Fuji_Photo": "🎞️ 후지필름 감성",
                        "Fuji_Compact": "👜 후지 똑딱이", "Pana_Video": "🎬 파나소닉 영상",
                        "Pana_M43": "🦅 파나소닉 망원", "Pocket_Cam": "🪄 포켓/짐벌캠", "Phone": "📱 스마트폰"
                    }
                    df_scores = pd.DataFrame({"카테고리": [display_names.get(k, k) for k in total_scores.keys()], "점수": list(total_scores.values())})
                    fig = px.line_polar(df_scores, r='점수', theta='카테고리', line_close=True, template="plotly_dark")
                    fig.update_traces(fill='toself', line_color='#4CAF50')
                    fig.update_layout(polar=dict(radialaxis=dict(visible=False, showticklabels=False)), margin=dict(l=40, r=40, t=40, b=40), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fig, width="stretch")

            # 탭2: 추천 카메라 세부 스펙 테이블로 렌더링
            with tab_specs:
                if "specs" in result:
                    st.table(pd.DataFrame(list(result["specs"].items()), columns=["스펙 항목", "세부 내용"]).set_index("스펙 항목"))

            # 탭3: 내가 선택한 답변 요약해서 보여주기
            with tab_answers:
                with st.container(height=500):
                    if "answers" in st.session_state and st.session_state.answers:
                        for q_idx, opt_idx in sorted(st.session_state.answers.items()):
                            st.markdown(f"**Q{q_idx + 1}. {quiz_data[q_idx]['question']}**")
                            st.caption(f"👉 {quiz_data[q_idx]['options'][opt_idx]['text']}")

        # 1위와 점수가 10점 미만: 경쟁 카메라 다이얼로그 트리거
        if close_competitors:
            if st.button("🔥 아쉽게 1위를 놓친 다른 카메라 보기", width="stretch"):
                show_competitors_dialog(close_competitors, result_data)