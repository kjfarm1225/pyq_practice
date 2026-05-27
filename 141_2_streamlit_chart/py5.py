import numpy as np
import pandas as pd
import streamlit as st

def sample():
    rng = np.random.default_rng()
    return pd.DataFrame(rng.integers(0, 10, (6, 3)), columns=["A", "B", "C"])

df = sample()
st.line_chart(df)

if st.button("DataFrame"):
    st.dataframe(df.T)