import pandas as pd
import streamlit as st

st.title("品質パトロールアプリ")

st.write("""
このアプリでは、拠点別の生産数・不具合数・ppmを確認します。
拠点を選択すると、その拠点の月別ppm推移グラフが表示されます。
最後に、最新月のppmから注意レベルを判定します。
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
selected_site = st.selectbox("確認する拠点を選択してください", site_list)

filtered_df = df[df["site"] == selected_site]
st.subheader("選択した拠点の品質データ")
st.dataframe(filtered_df)

total_production = filtered_df["production"].sum()
total_defects = filtered_df["defects"].sum()
average_ppm = (total_defects / total_production * 1000000).round(1)

st.subheader("集計結果")

st.write(f"総生産数:{total_production}個")
st.write(f"総不具合数:{total_defects}個")
st.write(f"平均ppm:{average_ppm}")

chart_df = filtered_df.set_index("month")[["ppm"]]

st.subheader("月別ppm推移グラフ")
st.line_chart(chart_df)

latest_month = filtered_df.iloc[-1]["month"]
latest_ppm = filtered_df.iloc[-1]["ppm"]

st.subheader("最新月の注意レベル")
st.write(f"最新月:{latest_month}")
st.write(f"最新ppm:{latest_ppm}")

if latest_ppm >= 5000:
    st.error("注意レベル：高いです。すぐに内容確認が必要です。")
elif latest_ppm >= 3000:
    st.warning("注意レベル：やや高めです。傾向確認をおすすめします。")
else:
    st.success("注意レベル：良好です。大きな問題はなさそうです。")

st.subheader("最後の行の確認")
st.dataframe(filtered_df)

st.write("最後の行はこちらです。")
st.write(filtered_df.iloc[-1])

latest_month = filtered_df.iloc[-1]["month"]
latest_ppm = filtered_df.iloc[-1]["ppm"]

st.write(f"取り出した月:{latest_month}")
st.write(f"取り出したppm:{latest_ppm}")