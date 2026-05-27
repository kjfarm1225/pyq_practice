import pandas as pd
import streamlit as st

st.title("品質アラート指令室")
st.write("""
このアプリでは拠点別の月別品質データを確認します。
""")

df = pd.DataFrame({
    "month": ["1月", "2月", "3月", "4月", "5月", "6月",
              "1月", "2月", "3月", "4月", "5月", "6月",
              "1月", "2月", "3月", "4月", "5月", "6月"],
    "site": ["MELMB", "MELMB", "MELMB", "MELMB", "MELMB", "MELMB",
             "WSE", "WSE", "WSE", "WSE", "WSE", "WSE",
             "SUS", "SUS", "SUS", "SUS", "SUS", "SUS"],
    "production": [1200, 1500, 1300, 1600, 1400, 1700,
                   1000, 1100, 1050, 1200, 1150, 1250,
                   900, 950, 1000, 1100, 1050, 1150],
    "defects": [4, 6, 3, 5, 2, 7,
                2, 5, 4, 3, 6, 4,
                1, 2, 2, 3, 5, 6],
})

df["ppm"] = (df["defects"] / df["production"] * 1000000).round(1)

site_list = df["site"].unique()
selected_site = st.selectbox("確認する拠点を選択してください。", site_list)
filtered_df = df[df["site"] == selected_site]

st.subheader("月別ppm推移グラフ")
chart_df = filtered_df.set_index("month")[["ppm"]]
st.line_chart(chart_df)

latest_month = filtered_df.iloc[-1]["month"]
latest_ppm = filtered_df.iloc[-1]["ppm"]

st.subheader("最新月の判定")

st.write(f"最新月:{latest_month}")
st.write(f"最新ppm:{latest_ppm}")

if latest_ppm >= 5000:
    st.error("注意レベル:高いです。すぐに内容確認が必要です。")
elif latest_ppm >= 4000:
    st.warning("注意レベル:やや高めです。傾向確認をおすすめします。")
else:
    st.success("注意レベル:良好です。大きな問題はなさそうです。")

if st.button("注意付きだけ表示"):
    alert_df = filtered_df[filtered_df["ppm"] >= 3000]
    st.subheader("ppmが3000以上の月")

    if len(alert_df) == 0:
        st.success("注意が必要な月はありません")
    else:
        st.dataframe(alert_df)

if st.button("転置データを表示"):
    st.subheader("転置したデータ")
    st.dataframe(filtered_df.T)