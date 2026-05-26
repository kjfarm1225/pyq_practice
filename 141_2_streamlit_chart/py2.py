# exercises

import pandas as pd
import streamlit as st

"""
# 月別不具合数グラフ

このアプリでは、月別の不具合数を表と折れ線グラフで確認します。

"""

df = pd.DataFrame({
    "defects": [4, 6, 3, 5, 2, 7]
}, index=["1月", "2月", "3月", "4月", "5月", "6月"])

st.subheader("月別不具合数データ")
st.dataframe(df)

st.subheader("月別不具合数グラフ")
st.line_chart(df)