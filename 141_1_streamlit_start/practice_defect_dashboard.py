# 応用練習
import pandas as pd
import streamlit as st

st.title("拠点別品質データ確認アプリ")
st.write("拠点を選択して、月別の生産数・不具合数・不良率ppmを確認します。")

df = pd.DataFrame({
    "month": ["1月", "1月", "2月", "2月", "3月", "3月"],
    "site": ["melmb", "wse", "melmb", "wse", "melmb", "wse"],
    "production":[1000, 1200, 1100, 1300, 1050, 1250],
    "defects": [4, 6, 3, 5, 2, 7],
})

df["ppm"] = (df["defects"] / df["production"] * 1000000).round(1)

site_list = df["site"].unique()
selected_site = st.selectbox("拠点を選択してください", site_list)
filtered_df = df[df["site"] == selected_site]
st.subheader("選択した拠点の品質データ")
st.dataframe(filtered_df)
if filtered_df.empty:
    st.warning("選択した拠点にデータがありません。別の拠点を選択してください。")

total_production = filtered_df["production"].sum()
total_defects = filtered_df["defects"].sum()

st.subheader("集計結果")

st.write(f"総生産数: {total_production}")
st.write(f"総不具合数: {total_defects}件")

if total_production > 0:
    average_ppm = (total_defects / total_production * 1000000).round(1)
    st.write(f"平均ppm: {average_ppm}")
else:
    st.write("平均ppm: データが不足しています（総生産数が0件）")