import pandas as pd
import streamlit as st

df = pd.DataFrame({
    "month": ["1月", "2月", "3月", "4月", "5月", "6月"],
    "production": [1000, 1200, 1150, 1300, 1250, 1400],
    "defects": [2, 5, 3, 9, 4, 10],
})

df["ppm"] = (df["defects"] / df["production"] * 1000000).round(1)

st.title("品質グラフ選択アプリ")
st.write("選択ボックスでグラフの種類を切り替えます。")

chart_df = df.set_index("month")[["ppm"]]
defect_chart_df = df.set_index("month")[["defects"]]

dc = {
    "折れ線グラフ": st.line_chart,
    "棒グラフ": st.bar_chart,
    "面グラフ": st.area_chart,
    "散布図": lambda data: st.scatter_chart(df, x="production", y="defects"),
    "不具合数 棒グラフ": lambda data: st.bar_chart(defect_chart_df),
}

kind = st.selectbox("グラフの種類", list(dc))

dc[kind](chart_df)

if st.checkbox("元データを表示する"):
    st.dataframe(df)