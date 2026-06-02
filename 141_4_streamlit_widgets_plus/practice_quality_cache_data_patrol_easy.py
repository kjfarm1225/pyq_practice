import pandas as pd
import streamlit as st


@st.cache_data
def load_data():
    df = pd.DataFrame({
        "month": ["1月", "2月", "3月"],
        "defects": [3, 7, 2]
    })
    return df

df =load_data()
st.dataframe(df)