import numpy as np
import pandas as pd
import streamlit as st

@st.cache
def sample():
    rng = np.random.default_rng()
    return pd.DataFrame(rng.integers(0, 10, (6, 3)), columns=["A", "B", "C"])

df = sample()
data = (10 - df).to_csv(index=False).encode()
st.sidebar.download_button("Download CSV", data, "sample.csv")

if file := st.sidebar.file_uploader('upload'):
    df = pd.read_csv(file)

dc = {
    "line": st.line_chart,
    "bar": st.bar_chart,
    "area": st.area_chart
}

kind = st.sidebar.selectbox("kind", list(dc))
sl = st.sidebar.slider("lower", 0, 4)
dc[kind](df[sl:])

if st.checkbox("DataFrame"):
    st.dataframe(df[sl:].T)
