# core/toolbox.py (캐싱함수 및 공통로직) 
import streamlit as st
import json
import os

# [공통] JSON 데이터 로딩함수
# 캐싱이 필요한 데이터로딩
@st.cache_data(show_spinner=True)
def load_json_data_cached(filename):
    print(f"[INFO]: 파일 시스템에서 {filename} 읽어캐싱하는 중...")
    return base_load_json_data(filename)

# 캐싱이 필요 없는 데이터로딩
def load_json_data(filename):
    return base_load_json_data(filename)

# base JSON로더
def base_load_json_data(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, ".." ,"data", filename)

    if not os.path.exists(file_path):
        return {}
        
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# result.json의 카메라 이미지 파일을 미리 캐싱
# 이미지 바이너리 캐싱 
@st.cache_data(show_spinner=True)
def get_image_bytes(image_path):

    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "..", image_path)

    if not os.path.exists(file_path):
        return None
    print(f"[INFO]: 파일 시스템에서 {image_path} 읽어 바이너리로 캐싱하는 중...")
    with open(file_path, "rb") as f:
        return f.read()
        
# 이미지 프리로딩
@st.cache_data(show_spinner=True)
def preload_all_camera_images(result_data):
    data_dict = result_data[0] if isinstance(result_data, list) else result_data
    
    for camera_key, camera_info in data_dict.items():
        if isinstance(camera_info, dict) and "image_url" in camera_info:
            image_path = camera_info["image_url"]
            # 캐싱 함수 호출
            print(f"[DEBUG]:이미지 {image_path}를 로딩하고 캐싱하는 중...")  # 로딩 중인 이미지 경로 출력 (디버깅용)
            get_image_bytes(image_path) # 바이너리로 캐싱하여 메모리에 올려둠 (캐싱 함수 내부에서 파일 존재 여부 체크)
            
    return True


# [공통] 로그인 권한 체크 
def check_login():
    if not st.session_state.get("logged_in", False):
        st.session_state.show_expire_warning = True
        st.switch_page("pages/1_landing.py")
        st.stop()

# [공통] 로그아웃 다이얼로그
@st.dialog("잠시만요!")
def show_logout_dialog():
    st.caption("정말로 로그아웃 하시겠어요?")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("네, 로그아웃 할래요", type="primary", width="stretch"):
            # 세션 초기화
            # 로그아웃 버튼을 눌렀을 때 실행하기 좋은 코드
            st.session_state.clear()
            st.switch_page("pages/1_landing.py")
            
    with col2:
        if st.button("취소", width="stretch"):
            st.rerun()