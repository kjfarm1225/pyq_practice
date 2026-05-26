import pandas as pd
import streamlit as st

"""
# 月別ｐｐｍ確認アプリ

このアプリでは、月別の生産数・不具合数・不良率ｐｐｍを確認します。

"""

df = pd.DataFrame({
    "month": ["1月", "2月", "3月", "4月", "5月", "6月"],
    "production": [1200, 1500, 1300, 1600, 1400, 1700],
    "defects": [4, 6, 3, 5, 2, 7]
})

df["ppm"] = (df["defects"] / df["production"] * 1000000).round(1)

st.subheader("月別品質データ")
st.dataframe(df)

chart_df = df.set_index("month")[["ppm"]]

st.subheader("月別ppm推移グラフ")
st.line_chart(chart_df)