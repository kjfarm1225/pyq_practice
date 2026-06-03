import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")

st.title("🛡️ 品質モンスター司令室 完全版")
st.write("品質CSVをアップロードすると、ppmを自動計算し、拠点別・期間別・グラフ種類別に品質モンスターを確認できます。")

template_df = pd.DataFrame({
    "month": [
        "1月", "2月", "3月", "4月", "5月", "6月",
        "1月", "2月", "3月", "4月", "5月", "6月",
        "1月", "2月", "3月", "4月", "5月", "6月",
    ],
    "site": [
        "MELMB", "MELMB", "MELMB", "MELMB", "MELMB", "MELMB",
        "WSE", "WSE", "WSE", "WSE", "WSE", "WSE",
        "GSE", "GSE", "GSE", "GSE", "GSE", "GSE",
    ],
    "production": [
        1000, 1200, 1150, 1300, 1250, 1400,
        900, 1000, 980, 1100, 1050, 1200,
        800, 850, 900, 950, 1000, 1050,
    ],
    "defects": [
        3, 7, 2, 8, 5, 4,
        2, 4, 9, 12, 5, 3,
        100, 3, 5, 7, 10, 4,
    ],
})

template_csv = template_df.to_csv(index=False).encode("utf-8-sig")

st.sidebar.download_button(
    "🧾 討伐用CSVひな形をダウンロード",
    template_csv,
    "quality_monster_tmplate.csv",
    "text/csv",
)

file = st.sidebar.file_uploader("📤 品質CSVをアップロード", type="csv")

if file is None:
    st.info("まずは左のボタンから討伐用CSVのひな形をダウンロードして、そのCSVをアップロードしてください。")
    st.subheader("📋 CSVひな形プレビュー")
    st.dataframe(template_df)
    st.stop()

df = pd.read_csv(file)

required_columns = ["month", "site", "production", "defects"]

if not all(column in df.columns for column in required_columns):
    st.error("csvに必要な列がありません。month, site, production, defectsの列が必要です。")
    st.stop()

if (df["production"] == 0).any():
    st.error("production列に0が含まれています。ppmを計算できないため、0以外の値を入力してください。")
    st.stop()

df["ppm"] = (df["defects"] / df["production"] * 1000000).round(1)

def judge_monster(ppm):
    if ppm >= 9000:
        return "🐉 ドラゴン級", "危険"
    elif ppm >= 5000:
        return "👹 オーガ級", "注意"
    else:
        return "👻 ファンタム級", "安全"

df[["monster", "judge"]] = df["ppm"].apply(lambda x: pd.Series(judge_monster(x)))

site_options = sorted(df["site"].dropna().unique())
selected_site = st.sidebar.selectbox("🏭 拠点を選んでください", site_options)

filtered_df = df[df["site"] == selected_site].reset_index(drop=True)

max_start = max(len(filtered_df) -2, 0)
start = st.sidebar.slider("📍 開始位置を選んでください", 0, max_start)

display_df = filtered_df.iloc[start:]

chart_target = st.sidebar.selectbox(
     "📊 グラフに表示する項目",
     ["ppm", "defects", "production"],
)

dc = {
    "折れ線グラフ": st.line_chart,
    "棒グラフ": st.bar_chart,
    "面グラフ": st.area_chart,
}

kind = st.sidebar.selectbox("📈 グラフの種類を選んでください", list(dc))

st.subheader(f"🏭 選択中の拠点：{selected_site}")
st.write("表示開始位置:", start)
st.write("グラフ表示項目:", chart_target)
st.write("グラフの種類:", kind)

chart_df = display_df.set_index("month")[[chart_target]]
dc[kind](chart_df)

latest_month = display_df.iloc[-1]["month"]
latest_ppm = display_df.iloc[-1]["ppm"]
latest_monster = display_df.iloc[-1]["monster"]
latest_judge = display_df.iloc[-1]["judge"]

st.subheader("🧭 最新月の品質モンスター判定")

col1, col2, col3, col4 = st.columns(4)

col1.metric("最新月", latest_month)
col2.metric("最新ppm", round(latest_ppm, 1))
col3.metric("モンスター", latest_monster)
col4.metric("判定", latest_judge)


if latest_judge == "危険":
    st.error("🐉 ドラゴン級です！すぐに原因確認・流出影響・対象範囲を確認しましょう。")
elif latest_judge == "注意":
    st.warning("👹 オーク級です。傾向確認と、前月比の変化を確認しましょう。")
else:
    st.success("👻 ファンタム級です。大きな問題はなさそうですが、引き続き品質管理をお願いします。")
    st.snow()

st.subheader("📋 表示中の品質データ")
st.dataframe(display_df)

if st.sidebar.checkbox("📋 全拠点データを表示する"):
    st.subheader("📋 全拠点データ")
    st.dataframe(df)

if st.sidebar.checkbox("📝 確認メモを表示する"):
    st.subheader("📝 確認メモ")
    st.write("・ppmが急上昇した月は、工程変更・部品ロット変更・検査条件変更を確認する")
    st.write("・不具合数だけでなく、生産数も一緒に見る")
    st.write("・最新月だけでなく、数か月の流れを見る")
    st.write("・ドラゴン級が出た場合は、対象範囲と流出有無を確認する")

result_csv = df.to_csv(index=False).encode("utf-8-sig")

st.sidebar.download_button(
    "🏆 討伐レポートCSVをダウンロード",
    result_csv,
    "quality_monste_result.csv",
    "text/csv",
)