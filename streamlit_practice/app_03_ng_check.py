#ライブラリー読み込み
import streamlit as st
import pandas as pd

#画面の基本設定
st.set_page_config(
    page_title="LCM不具合データNG確認",
    layout="wide",
)

st.title("LCM不具合データ NG確認アプリ")

#ブロック3：CSVアップロード
uploaded_file = st.file_uploader(
    "CSVファイルをアップロードしてください",
    type=["csv"],
)

#ブロック4：CSVがアップロードされた場合だけ処理する
if uploaded_file is not None:

    #csvをそのまま読み込む
    df = pd.read_csv(uploaded_file, encoding="utf-8-sig")

    #元データを表示する
    st.subheader("1. アップロードされた元データ")
    st.dataframe(df, use_container_width=True)

    #必要な列を確認する
    required_columns = [
        "defect_qty",
        "inspection_qty",
        "occ_at_jst",
    ]

    missing_columns = []

    for column in required_columns:
        if column not in df.columns:
            missing_columns.append(column)

    if len(missing_columns) > 0:
        st.error(f"必要な列がありません: {missing_columns}")
        st.stop()

    #ブロック8：加工用データを作成する
    df_work = df.copy()

    #ブロック9：日時列をきれいにする
    df_work["occ_at_jst_raw"] = df_work["occ_at_jst"]

    df_work["occ_at_jst_clean"] = (
        df_work["occ_at_jst"]
        .astype("string")
        .str.strip()
    )

    #ブロック10：数値型に変換する
    df_work["defect_qty_num"] = pd.to_numeric(
        df_work["defect_qty"],
        errors="coerce",
    )

    df_work["inspection_qty_num"] = pd.to_numeric(
        df_work["inspection_qty"],
        errors="coerce",
    )

    #ブロック11：日付型に変換する
    df_work["occ_at_jst_dt"] = pd.to_datetime(
        df_work["occ_at_jst_clean"],
        errors="coerce",
    )

    #ブロック12：表示列を決める
    display_columns = [
        "defect_id",
        "site",
        "model",
        "defect_category",
        "defect_qty",
        "defect_qty_num",
        "inspection_qty",
        "inspection_qty_num",
        "occ_at_jst",
        "occ_at_jst_dt",
        "status",
    ]

    display_columns = [
        column for column in display_columns
        if column in df_work.columns
    ]

    #ブロック13：変換後データを表示する
    st.subheader("2. 変換後データ")

    st.dataframe(
        df_work[display_columns],
        use_container_width=True
    )

    #ブロック14：NG件数を計算する
    defect_qty_ng_count = df_work["defect_qty_num"].isna().sum()
    inspection_qty_ng_count = df_work["inspection_qty_num"].isna().sum()
    date_ng_count = df_work["occ_at_jst_dt"].isna().sum()

    #ブロック15：NG件数を表示する
    st.subheader("3.変換NG件数")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("defect_qty 数値変換NG", defect_qty_ng_count)

    with col2:
        st.metric("inspection_qty 数値変換NG", inspection_qty_ng_count)

    with col3:
        st.metric("occ_at_jst 日時変換NG", date_ng_count)