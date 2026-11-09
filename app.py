# 📋 app.py · [실습 4-1 + 도전] 화면은 Streamlit, 일은 API 가 — 접근 코드를 헤더에 실어 /explain 을 부름 (설명 한 번에 요청 1번)
import requests
import streamlit as st

try:
    API_URL = st.secrets["API_URL"]                  # Community Cloud 에 올릴 때는 Secrets 에 API 주소
except Exception:
    API_URL = "http://localhost:8000"                # Colab 에서 점검할 때는 같은 런타임의 API 서버

try:
    ACCESS_CODE = st.secrets["APP_ACCESS_CODE"]      # 접근 코드도 Secrets 에서만 읽음 (코드에 적지 않음)
except Exception:
    ACCESS_CODE = ""                                 # 접근 코드를 쓰지 않는 서버면 빈 값

st.title("📝 AI 용어 설명기 (API 버전)")
st.caption(f"API 주소 : {API_URL}")

style = st.selectbox("말투", ["초등학생도 알아듣게 쉽게", "전공 수업처럼 정확하게", "재미있는 비유를 들어"])
word = st.text_input("궁금한 용어", placeholder="예: API · 토큰 · 서버")

if st.button("설명 듣기", disabled=(word.strip() == "")):
    with st.spinner("API 에 묻는 중..."):
        try:
            response = requests.post(
                f"{API_URL}/explain",
                json={"word": word, "style": style},
                headers={"X-Access-Code": ACCESS_CODE},     # ← 추가된 부분
                timeout=90,
            )
        except requests.RequestException:
            st.error("❌ API 서버에 닿지 못함 — 서버가 켜져 있는지, 주소가 맞는지 확인하세요.")
        else:
            if response.status_code == 200:
                data = response.json()
                st.markdown(data["answer"])
                st.caption(f"상태 번호 200 · 토큰 {data['tokens']}")
            else:
                st.error(f"❌ 상태 번호 {response.status_code} : {response.json().get('detail')}")
