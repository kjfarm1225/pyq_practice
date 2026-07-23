import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="LCM不具合データビューア",
    layout="wide",
)
st.title("LCM不具合データビューア")

uploaded_file = st.file_uploader(
    "csvファイルをアップロードしてください",
    type=["csv"],
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("アップロードされたcsvデータ")
    st.dataframe(df, use_container_width=True)

    st.subheader("データ件数")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("行数", df.shape[0])

    with col2:
        st.metric("列数", df.shape[1])

    st.subheader("列名")
    st.write(df.columns.tolist())

else:
    st.info("csvファイルをアップロードしてください")