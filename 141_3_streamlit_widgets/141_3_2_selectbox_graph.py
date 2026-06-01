import numpy as np
import pandas as pd
import streamlit as st

@st.cache
def sample():
    rng = np.random.default_rng()
    return pd.DataFrame(rng.integers(0, 10, (6, 3)), columns=["A", "B", "C"])

df = sample()

# グラフのコマンドを値とする辞書
dc = {"line": st.line_chart, "bar": st.bar_chart, "area": st.area_chart}
kind = st.selectbox("kind", list(dc))
dc[kind](df)

if st.checkbox("DataFrame"):
    st.dataframe(df.T)