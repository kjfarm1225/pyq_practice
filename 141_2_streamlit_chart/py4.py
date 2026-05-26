import pandas as pd
import streamlit as st

df = pd.DataFrame({
    "month": ["1月", "2月", "3月", "4月"],
    "production": [1200, 1500, 1300, 1600],
    "defects": [4, 6, 3, 5],
})

df["ppm"] = (df["defects"] / df["production"] * 1000000).round(1)

st.subheader("元の表")
st.dataframe(df)

#chart_df = df.set_index("month")[["ppm"]]
temp_df = df.set_index("month")
chart_df = temp_df[["ppm"]]
st.subheader("グラフ用の表")
st.dataframe(chart_df)

st.subheader("月別ppmグラフ")
st.line_chart(chart_df)