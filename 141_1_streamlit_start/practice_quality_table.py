import pandas as pd
import streamlit as st

st.title("月別　品質データ確認")
st.write("各月の生産数、不具合数、不良率ppmを確認するための簡単な表です。")

df = pd.DataFrame({
    "month": ["1月", "2月", "3月", "4月"],
    "site": ["melmb", "melmb", "melmb", "melmb"],
    "production": [1200, 1500, 1300, 1600],
    "defects": [4, 6, 3, 5],

})

df["ppm"] = (df["defects"] / df["production"] * 1000000).round(1)

st.dataframe(df)