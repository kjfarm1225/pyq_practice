import pandas as pd
import streamlit as st

df = pd.DataFrame({
    "month": ["1月", "2月", "3月", "4月", "1月", "2月", "3月", "4月", "1月", "2月", "3月", "4月", "1月", "2月", "3月", "4月"],
    "site": ["MELMB", "MELMB", "MELMB", "MELMB", "WSE", "WSE", "WSE", "WSE", "GSE", "GSE", "GSE", "GSE", "ISE", "ISE", "ISE", "ISE"],
    "production": [1000, 1200, 1150, 1300, 900, 1000, 980, 1100, 800, 850, 900, 950, 700, 750, 780, 800],
    "defects": [3, 7, 2, 8, 2, 4, 6, 3, 1, 3, 5, 7, 1, 2, 4, 6],
})

df["ppm"] = (df["defects"] / df["production"] * 1000000).round(1)

st.title("🛰️ 品質サイドバー管制室 ISE追加・拠点自動取得版")
st.write("サイドバーで拠点とグラフ種類を選び、月別ppmを確認します。")

site_options = sorted(df["site"].dropna().unique())
selected_site = st.sidebar.selectbox("拠点を選んでください", site_options)

filtered_df = df[df["site"] == selected_site]

chart_df = filtered_df.set_index("month")[["ppm"]]

dc = {
    "折れ線グラフ": st.line_chart,
    "棒グラフ": st.bar_chart,
    "面グラフ": st.area_chart,
}

kind = st.sidebar.selectbox("グラフの種類を選んでください", list(dc))

st.write("選択中の拠点:", selected_site)

dc[kind](chart_df)

latest_month = filtered_df.iloc[-1]["month"]
latest_ppm = filtered_df.iloc[-1]["ppm"]

st.write("最新月:", latest_month)
st.write("最新ppm:", latest_ppm)

if latest_ppm >= 7000:
    st.error("🚨 危険レベル：ppmが高いです。すぐに内容確認が必要です。")
elif latest_ppm >= 4000:
    st.warning("⚠️ 注意レベル：ppmがやや高めです。傾向確認をおすすめします。")
else:
    st.success("✅ 良好レベル：大きな問題はなさそうです。")

if st.sidebar.checkbox("元データを表示する"):
    st.dataframe(filtered_df)

if st.sidebar.checkbox("全拠点データを表示する"):
    st.dataframe(df)

if st.sidebar.checkbox("確認メモを表示する"):
    st.write("確認ポイント")
    st.write("・最新月だけd無く、数か月の流れを見る")
    st.write("・不具合数だけでなく、生産数も一緒にみる")
    st.write("・ppmが急に上がった月は、工程変化や部品ロット変更を確認する")
