import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

#文字化け対策
plt.rcParams["font.family"] = "Meiryo"
plt.rcParams["axes.unicode_minus"] = False

st.title("拠点別　品質確認ダッシュボード")
st.write("拠点を選択して、月別の生産数・不具合数・不良率ppmを確認します。")

#品質データ作成
df = pd.DataFrame({
    "month": ["1月", "1月", "1月",
              "2月", "2月", "2月",
              "3月", "3月", "3月",
              "4月", "4月", "4月"],
        "site": ["MELMB", "WSE", "SUS",
             "MELMB", "WSE", "SUS",
             "MELMB", "WSE", "SUS",
             "MELMB", "WSE", "SUS"],
    "production": [1200, 1000, 900,
                   1500, 1100, 950,
                   1300, 1050, 1000,
                   1600, 1200, 1100],
    "defects": [4, 2, 1,
                6, 5, 2,
                3, 4, 2,
                5, 3, 3],
})

#ppm calculation

df["ppm"] = (df["defects"] / df["production"] * 1000000).round(1)

#拠点選択

site_list = df["site"].unique()
selected_site = st.selectbox("拠点を選択してください", site_list)

#選択された拠点のデータをフィルタリング
filtered_df = df[df["site"] == selected_site]

st.subheader("選択した拠点の品質データ")
st.dataframe(filtered_df)

#集計する
total_production = filtered_df["production"].sum()
total_defects = filtered_df["defects"].sum()
average_ppm = (total_defects / total_production * 1000000).round(1)

st.subheader("集計結果")

st.write(f"総生産数:{total_production}個")
st.write(f"総不具合数:{total_defects}個")
st.write(f"平均ppm:{average_ppm}")

#ppmグラフ作成

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(filtered_df["month"], filtered_df["ppm"], marker="o")

for month, ppm, defects in zip(filtered_df["month"], filtered_df["ppm"], filtered_df["defects"]):
    ax.text(month, ppm + 10, f"{defects}件", ha="center")

ax.set_title(f"{selected_site}月別ppm推移")
ax.set_xlabel("月")
ax.set_ylabel("ppm")
ax.grid(True)

st.pyplot(fig)