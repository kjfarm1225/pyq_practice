import streamlit as st
import pandas as pd
from pathlib import Path

st.header("数学の試験の成績の検索")
csv_path = Path(__file__).parent / "input" / "exam.csv"
df = pd.read_csv(csv_path, encoding="utf-8-sig")
s = st.text_input("クエリ")

if s:
    try:
        result = df.query(s)
        st.dataframe(result)
    except:
        st.error("クエリを正しくしてください")
