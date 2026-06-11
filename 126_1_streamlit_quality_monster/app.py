import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="品質モンスター司令室",
    layout="wide"
)

st.title("🛡️ 品質モンスター司令室 Streamlit版")
st.write("CSVをアップロードして、欠損値・統計量・PPM・危険ランク・グラフを確認します。")


plt.rcParams["font.family"] = "Meiryo"


@st.cache_data
def make_sample_df():
    df_sample = pd.DataFrame(
        [
            ["2026/06/01", "MELMB", "LCM-A", "点灯不良", 10000, 3],
            ["2026/06/01", "WSE", "LCM-B", "外観不良", 8000, 5],
            ["2026/06/02", "GSE", "LCM-C", "ショート", 12000, 1],
            ["2026/06/02", "MELMB", "LCM-A", "点灯不良", 11000, 8],
            ["2026/06/03", "ISE", "LCM-D", "コネクタ浮き", 9000, 2],
            ["2026/06/03", "WSE", "LCM-B", "異物混入", 7000, 7],
            ["2026/06/04", "MELAC", "LCM-E", "はんだ不良", 15000, 4],
            ["2026/06/04", "GSE", "LCM-C", "ショート", 10000, 6],
            ["2026/06/05", "MELMB", "LCM-A", "点灯不良", 9000, 10],
            ["2026/06/05", "ISE", "LCM-D", "コネクタ浮き", 8500, 0],
            ["2026/06/06", "WSE", "LCM-B", "外観不良", 9000, np.nan],
            ["2026/06/06", "MELAC", "LCM-E", "はんだ不良", 14000, 9],
        ],
        columns=["date", "site", "product", "defect", "production", "defects"],
    )
    return df_sample


def read_uploaded_csv(uploaded_file):
    try:
        return pd.read_csv(uploaded_file, encoding="utf-8-sig")
    except UnicodeDecodeError:
        uploaded_file.seek(0)
        return pd.read_csv(uploaded_file, encoding="Shift_JIS")


df_sample = make_sample_df()

sample_csv = df_sample.to_csv(index=False).encode("utf-8-sig")

st.download_button(
    label="📥 サンプルCSVをダウンロード",
    data=sample_csv,
    file_name="quality_monster_patrol.csv",
    mime="text/csv"
)


uploaded_file = st.file_uploader(
    "品質CSVをアップロードしてください",
    type=["csv"]
)

if uploaded_file is None:
    st.info("CSVが未アップロードなので、サンプルデータで表示しています。")
    df = df_sample.copy()
else:
    df = read_uploaded_csv(uploaded_file)


required_columns = ["date", "site", "product", "defect", "production", "defects"]

missing_columns = []

for column in required_columns:
    if column not in df.columns:
        missing_columns.append(column)

if len(missing_columns) > 0:
    st.error("必要な列が足りません。")
    st.write("足りない列:", missing_columns)
    st.stop()


df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["production"] = pd.to_numeric(df["production"], errors="coerce")
df["defects"] = pd.to_numeric(df["defects"], errors="coerce")


st.subheader("📋 読み込んだデータ")
st.dataframe(df)


st.subheader("🧪 欠損値チェック")
missing_count = df.isna().sum()
st.dataframe(missing_count)


st.subheader("📊 production / defects の統計量")
st.dataframe(df[["production", "defects"]].describe())


df_valid = df.dropna(subset=["date", "production", "defects"]).copy()

df_valid["PPM"] = df_valid["defects"] / df_valid["production"] * 1000000
df_valid["PPM"] = df_valid["PPM"].round(1)

df_valid["危険ランク"] = np.where(
    df_valid["PPM"] >= 1000,
    "S級モンスター",
    np.where(
        df_valid["PPM"] >= 500,
        "A級モンスター",
        "通常モンスター"
    )
)


st.sidebar.header("🔍 表示条件")

site_list = sorted(df_valid["site"].unique())

selected_sites = st.sidebar.multiselect(
    "拠点を選んでください",
    site_list,
    default=site_list
)

min_ppm = st.sidebar.slider(
    "表示する最小PPM",
    min_value=0,
    max_value=1500,
    value=0,
    step=100
)

df_filtered = df_valid[
    (df_valid["site"].isin(selected_sites)) &
    (df_valid["PPM"] >= min_ppm)
].copy()

df_sorted = df_filtered.sort_values(by="PPM", ascending=False)

df_danger = df_sorted[df_sorted["危険ランク"] != "通常モンスター"]


st.subheader("🚨 品質モンスターランキング")

col1, col2, col3 = st.columns(3)

col1.metric("対象データ件数", len(df_sorted))
col2.metric("危険モンスター件数", len(df_danger))

if len(df_sorted) > 0:
    max_ppm = df_sorted["PPM"].max()
else:
    max_ppm = 0

col3.metric("最大PPM", max_ppm)


st.dataframe(df_sorted)


st.subheader("📈 PPMランキング 棒グラフ")

if len(df_sorted) == 0:
    st.warning("表示できるデータがありません。条件を変更してください。")
else:
    fig, ax = plt.subplots(figsize=(10, 6))

    x_labels = df_sorted["site"] + "_" + df_sorted["defect"]

    ax.bar(x_labels, df_sorted["PPM"])

    ax.set_title("品質モンスター PPMランキング")
    ax.set_xlabel("拠点_不具合")
    ax.set_ylabel("PPM")

    plt.xticks(rotation=45)

    st.pyplot(fig)


st.subheader("📉 日別 合計不良数の推移")

if len(df_filtered) == 0:
    st.warning("折れ線グラフに表示できるデータがありません。")
else:
    df_daily = df_filtered.groupby("date")["defects"].sum()

    fig2, ax2 = plt.subplots(figsize=(8, 5))

    ax2.plot(df_daily.index, df_daily.values, marker="o")

    ax2.set_title("日別 合計不良数の推移")
    ax2.set_xlabel("日付")
    ax2.set_ylabel("合計不良数")

    ax2.set_yticks(np.arange(0, 21, 5))

    plt.xticks(rotation=45)

    st.pyplot(fig2)


st.subheader("💾 CSVダウンロード")

report_csv = df_sorted.to_csv(index=False).encode("utf-8-sig")
danger_csv = df_danger.to_csv(index=False).encode("utf-8-sig")

st.download_button(
    label="📥 全件レポートCSVをダウンロード",
    data=report_csv,
    file_name="quality_monster_report.csv",
    mime="text/csv"
)

st.download_button(
    label="📥 危険モンスターCSVをダウンロード",
    data=danger_csv,
    file_name="danger_monster_report.csv",
    mime="text/csv"
)