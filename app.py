import sqlite3
import pandas as pd
import streamlit as st

# DB 경로
DB_PATH = "cve_intel_test.db"

# 데이터 로딩 함수
def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT id, published, description, gpt_summary FROM cve_data ORDER BY published DESC", conn)
    conn.close()
    return df

# Streamlit 설정
st.set_page_config(page_title="CISA KEV 요약 대시보드", layout="wide")

# 💡 스타일 정의 (폰트 + 다크/라이트 대응)
st.markdown(
    """
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }

    .cve-title {
        font-size: 20px;
        font-weight: bold;
        color: #007acc;
    }

    .cve-desc {
        font-size: 16px;
        color: #666;
        margin-bottom: 10px;
    }

    .cve-summary {
        background-color: rgba(240, 240, 240, 0.05);
        color: #e0e0e0;
        border-left: 4px solid #007acc;
        padding: 14px;
        border-radius: 10px;
        line-height: 1.6;
        font-size: 15px;
        transition: background-color 0.3s ease;
    }

    @media (prefers-color-scheme: light) {
        .cve-summary {
            background-color: #f5f5f5;
            color: #333333;
            border-left: 4px solid #007acc;
        }
        .cve-desc {
            color: #333;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 앱 제목 ---
st.title("🛡️ Newest Exploited Vulnerabilities (CISA KEV)")

# --- 데이터 로딩 ---
df = load_data()

if df.empty:
    st.warning("최근 5일 이내 CISA KEV 데이터가 없습니다.")
else:
    # --- 사이드바 필터 ---
    # with st.sidebar:
    #     st.subheader("🔍 필터")
    #     search_term = st.text_input("CVE ID 또는 제품명으로 검색")
    #     if search_term:
    #         df = df[df["id"].str.contains(search_term, case=False) | df["description"].str.contains(search_term, case=False)]

    st.markdown(f"**최근 공격에 사용된 취약점 : {len(df)}개**")

    # --- 데이터 렌더링 ---
    for idx, row in df.iterrows():
        with st.expander(f"📎 {row['id']} ----  {row['description']}"):
            st.markdown("📅 **Date**")
            st.markdown(f"{row['published']}")

            st.markdown("🧠 **Summary**")
            st.markdown(f"<div class='cve-summary'>{row['gpt_summary'].replace('\n','<br>')}</div>", unsafe_allow_html=True)
