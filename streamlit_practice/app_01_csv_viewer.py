import streamlit as st
import pandas as pd

st.title("LCM不具合データviewer")

uploaded_file = st.file_uploader(
    "plsase upload a csv file",
    type=["csv"],
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.write("アップロードされたcsvデータ:")
    st.dataframe(df)

    st.write("行数・列数:")
    st.write(df.shape)

    st.write("列名:")
    st.write(df.columns.tolist())
else:
    st.write("please upload a csv file to view the data.")