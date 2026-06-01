import pandas as pd
import streamlit as st


df = pd.DataFrame({
    "month": ["1月", "2月", "3月", "4月"],
    "site": ["MELMB", "MELMB", "MELMB", "MELMB"],
    "production": [1000, 1200, 1100, 1300],
    "defects": [3, 7, 2, 8],
})

df["ppm"] = (df["defects"] / df["production"] * 1000000).round(1)

st.title("品質データ チェックボックス練習アプリ")

st.write("月別の不良率ppmを確認します。")

chart_df = df.set_index("month")[["ppm"]]

st.line_chart(chart_df)

latest_month = df.iloc[-1]["month"]
latest_ppm = df.iloc[-1]["ppm"]

st.write("最新月:", latest_month)
st.write("最新ppm:", latest_ppm)

if latest_ppm >= 5000:
    st.error("注意レベル：高いです。すぐに内容確認が必要です。")
elif latest_ppm >= 3000:
    st.warning("注意レベル：やや高めです。傾向確認をおすすめします。")
else:
    st.success("注意レベル：良好です。大きな問題はなさそうです。")

if st.checkbox("元データを表示する"):
    st.dataframe(df)

if st.checkbox("転置したデータを表示する"):
    st.dataframe(df.T)

if st.checkbox("ppmが3000以上のデータだけ表示する"):
    alert_df = df[df["ppm"] >= 3000]
    st.dataframe(alert_df)