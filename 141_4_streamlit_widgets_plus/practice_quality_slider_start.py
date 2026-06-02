import pandas as pd
import streamlit as st

df = pd.DataFrame({
    "month": ["1月", "2月", "3月", "4月", "5月", "6月"],
    "production": [1000, 1200, 1150, 1300, 1250, 1400],
    "defects": [3, 7, 2, 8, 5, 4],
})

df["ppm"] = (df["defects"] / df["production"] * 1000000).round(1)

st.set_page_config(layout="wide")
st.title("📊 品質データ 開始位置スライダー")
st.write("サイドバーのスライダーで、何月からグラフに使うかを選びます。")

start = st.sidebar.slider("開始位置", 0, 4)
chart_df = df[start:].set_index("month")[["ppm"]]

st.line_chart(chart_df)

if st.checkbox("使用データを表示する"):
    st.dataframe(df[start:])