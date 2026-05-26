# 練習問題　応用2
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

plt.rcParams["font.family"] = "Meiryo"
plt.rcParams["axes.unicode_minus"] = False

st.title("月別不良率ppmグラフ")

df = pd.DataFrame({
    "month": ["1月", "2月", "3月", "4月"],
    "production": [1200, 1500, 1300, 1600],
    "defects": [4, 6, 3, 5],
})

df["ppm"] = (df["defects"] / df["production"] * 1000000).round(1)

fig, ax = plt.subplots()
ax.plot(df["month"], df["ppm"], marker="o")

for month, ppm, defects in zip(df["month"], df["ppm"], df["defects"]):
    ax.text(month, ppm + 20, f"{defects}件", ha="center")

ax.set_xlabel("月")
ax.set_ylabel("不良率(ppm)")
ax.set_title("月別不良率ppm推移")
ax.grid(True)

st.pyplot(fig)