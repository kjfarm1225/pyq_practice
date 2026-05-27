import pandas as pd
import streamlit as st

st.title("品質データ確認アプリ")

df = pd.DataFrame({
    "month": ["1月", "2月", "3月", "4月"],
    "production": [1200, 1500, 1300, 1600],
    "defects": [4, 6, 3, 5],
})

df["ppm"] = (df["defects"] / df["production"] * 1000000).round(1)

chart_df = df.set_index("month")[["ppm"]]

st.subheader("月別ppmグラフ")
st.line_chart(chart_df)

if st.button("詳細データを表示"):
    st.subheader("月別品質データ")
    st.dataframe(df)