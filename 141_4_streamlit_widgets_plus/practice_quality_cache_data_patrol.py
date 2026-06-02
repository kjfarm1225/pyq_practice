import time
from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")

@st.cache_data
def load_quality_data():
    time.sleep(2)

    df = pd.DataFrame({
        "month": ["1月", "2月", "3月", "4月", "5月", "6月",
                  "1月", "2月", "3月", "4月", "5月", "6月",
                  "1月", "2月", "3月", "4月", "5月", "6月"],
        "site": ["MELMB", "MELMB", "MELMB", "MELMB", "MELMB", "MELMB",
                 "WSE", "WSE", "WSE", "WSE", "WSE", "WSE",
                 "GSE", "GSE", "GSE", "GSE", "GSE", "GSE"],
        "production": [1000, 1200, 1150, 1300, 1250, 1400,
                       900, 1000, 980, 1100, 1050, 1200,
                       800, 850, 900, 950, 1000, 1050],
        "defects": [3, 7, 2, 8, 5, 4,
                    2, 4, 6, 3, 9, 5,
                    1, 3, 5, 7, 4, 10],
    })

    df["ppm"] = (df["defects"] / df["production"] * 1000000).round(1)
    loaded_at = datetime.now().strftime("%H:%M:%S")

    return df, loaded_at

df, loaded_at = load_quality_data()

screen_time = datetime.now().strftime("%H:%M:%S")

st.title("品質データ　パトロール室")
st.write("st.cache_dataをつかてデータ読み込みをキャッシュする練習です。")

st.write("データ作成時刻:", loaded_at)
st.write("画面更新時間:", screen_time)

site_options = sorted(df["site"].dropna().unique())
selected_site = st.sidebar.selectbox("拠点を選んでください", site_options)

start = st.sidebar.slider("開始位置", 0, 4)
filtered_df = df[df["site"] == selected_site]
display_df = filtered_df[start:]
chart_df = display_df.set_index("month")[["ppm"]]

st.write("選択中の拠点:", selected_site)
st.line_chart(chart_df)

latest_month = display_df.iloc[-1]["month"]
latest_ppm = display_df.iloc[-1]["ppm"]

st.write("最新月:", latest_month)
st.write("最新ppm:", latest_ppm)

if latest_ppm >= 8000:
    st.error("危険レベル：ppmが高いです。すぐに確認しましょう。")
elif latest_ppm >= 5000:
    st.warning("注意レベル:ppmがややたかめです。 傾向確認しましょう。")
else:
    st.success("良好レベル:大きな問題はなさそうです。")

if st.sidebar.checkbox("全データを表示する"):
    st.dataframe(df)