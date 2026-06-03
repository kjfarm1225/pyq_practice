import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")

st.title("品質csv受付カウンター")
st.write("品質データcsvをアップロードすると、ppmを自動計算してグラフを表示します。")

template_df = pd.DataFrame({
    "month": ["1月", "2月", "3月", "4月"],
    "site": ["melmb", "melmb", "melmb", "melmb"],
    "production": [1000, 1200, 1150, 1300],
    "defects": [3, 7, 2, 2],
})

template_csv = template_df.to_csv(index=False).encode("utf-8-sig")

st.sidebar.download_button(
    "ひな形ｃｓｖをダウンロード",
    template_csv,
    "quality_template.csv",
    "text/csv",
)

file = st.sidebar.file_uploader("品質csvをアップロード", type="csv")

if file is None:
    st.info("まずは左のボタンからひな形csvをダウンロードして、そのcsvをアップロードしてください。")
    st.dataframe(template_df)
    st.stop()

df = pd.read_csv(file)

df["ppm"] = (df["defects"] / df["production"] * 1000000).round(1)

latest_ppm = df.iloc[-1]["ppm"]

if latest_ppm >= 7000:
    result = "危険"
elif latest_ppm >= 4000:
    result = "注意"
else:
    result = "良好"

df["judge"] = ""
df.loc[df.index[-1], "judge"] = result

st.subheader("アップロードされた品質データ")
st.dataframe(df)

chart_df = df.set_index("month")[["ppm"]]

st.subheader("ppm推移グラフ")
st.line_chart(chart_df)

st.write("最新ppm", round(latest_ppm, 1))
st.write("判定", result)

if result == "危険":
    st.error("危険レベル：すぐに内容確認が必要です。")
elif result == "注意":
    st.warning("注意レベル：傾向確認をお勧めします。")
else:
    st.success("良好レベル:大きな問題はなさそうです。")

result_csv =df.to_csv(index=False).encode("utf-8-sig")

st.sidebar.download_button(
    "判定結果csvをダウンロード",
    result_csv,
    "qulity_result.csv",
    "text/csv",
)