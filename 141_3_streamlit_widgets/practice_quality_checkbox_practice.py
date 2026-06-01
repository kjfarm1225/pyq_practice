import pandas as pd
import streamlit as st

df = pd.DataFrame({
    "month": ["1月", "2月", "3月", "4月", "5月", "6月"],
    "production": [1000, 1200, 1150, 1300, 1250, 1400],
    "defects": [2, 5, 3, 9, 4,10],
})

df["ppm"] = (df["defects"]  / df["production"] * 1000000).round(1)

st.title("品質グラフ選択アプリ")
st.write("グラフの種別を選んで、月別のppmを確認します。")

chart_df = df.set_index("month")[["ppm"]]

dc = {
    "line": st.line_chart,
    "bar": st.bar_chart,
    "area": st.area_chart,
}

kind = st.selectbox("グラフの種類", list(dc))

dc[kind](chart_df)

if st.checkbox("元データを表示する"):
    st.dataframe(df)