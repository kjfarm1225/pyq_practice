import streamlit as st
import pandas as pd

# ============================================================
# 1. Streamlit画面の基本設定
# ============================================================
# page_title：ブラウザのタブに表示される名前
# layout="wide"：画面を横に広く使う設定

st.set_page_config(
    page_title="LCM不具合データ変換チェック",
    layout="wide",
)

# ============================================================
# 2. アプリのタイトル表示
# ============================================================
# 画面の一番上に大きなタイトルを表示する

st.title("LCM不具合データ変換チェックアプリ")

# ============================================================
# 3. CSVファイルをアップロードする部品
# ============================================================
# st.file_uploader() で、CSVファイルを選ぶボタンを作る
# type=["csv"] にすることで、CSVファイルだけを選びやすくする

uploaded_file = st.file_uploader(
    "csvファイルをアップロードしてください",
    type=["csv"],
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file, encoding="utf-8-sig")

    # 元データ表示
    st.subheader("1.アップロードされた元データ")
    st.dataframe(df, use_container_width=True)

    # 必要列の確認
    required_columns =[
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

    # 加工用データを作成
    df_work = df.copy()

    # 日時列の元データ保存と空白除去
    df_work["occ_at_jst_raw"] = df_work["occ_at_jst"]

    df_work["occ_at_jst_clean"] = (
        df_work["occ_at_jst"]
        .astype("string")
        .str.strip()
    )

    # 数値変換
    df_work["defect_qty_num"] = pd.to_numeric(
        df_work["defect_qty"],
        errors="coerce",
    )

    df_work["inspection_qty_num"] = pd.to_numeric(
        df_work["inspection_qty"],
        errors="coerce",
    )

    # 日時変換
    df_work["occ_at_jst_dt"] = pd.to_datetime(
        df_work["occ_at_jst_clean"],
        errors="coerce",
    )

    # 変換後のデータ表示例
    display_columns = [
        "defect_id",
        "site",
        "model",
        "defect_category",
        "defect_qty",
        "defect_qty_num",
        "inspection_qty_num",
        "occ_at_jst",
        "occ_at_jst_dt",
        "status",
    ]

    # 変換後データ表示
    st.subheader("2.変換後データ")

    # 存在しない列を参照するとKeyErrorになるため、存在する列のみ表示する
    available_display_columns = [c for c in display_columns if c in df_work.columns]

    st.dataframe(
        df_work[available_display_columns],
        use_container_width=True,
    )

    # 変換ng件数を計算
    defect_qty_ng_count = df_work["defect_qty_num"].isna().sum()
    inspection_qty_ng_count = df_work["inspection_qty_num"].isna().sum()
    data_ng_count = df_work["occ_at_jst_dt"].isna().sum()

    # 変換ng件数を表示
    st.subheader("3.変換NG件数")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("defect_qty 数値変換ng", defect_qty_ng_count)

    with col2:
        st.metric("inspection_qty 数値変換ng", inspection_qty_ng_count)

    with col3:
        st.metric("日時変換ng", data_ng_count)

    # データ型確認用の表作成
    dtype_series = df_work[
        [
            "defect_qty",
            "inspection_qty_num",
            "occ_at_jst_dt",
        ]
    ].dtypes.astype(str)

    dtype_df = dtype_series.reset_index()
    dtype_df.columns = pd.Index([
        "列名",
        "データ型",
    ])

    # データ型表示
    st.subheader("4.変換後のデータ型")
    st.dataframe(dtype_df, use_container_width=True)

# CSV未アップロード時の表示
else:
    st.info("CSVファイルをアップロードしてください。")