import time
from io import StringIO

import pandas as pd
import streamlit as st

CSV_TEXT = """
month,site,production,defects
1月,MELMB,1200,4
2月,MELMB,1500,6
3月,MELMB,1300,3
4月,MELMB,1600,5
1月,WSE,1000,2
2月,WSE,1100,5
3月,WSE,1050,4
4月,WSE,1200,3
1月,SUS,900,1
2月,SUS,950,2
3月,SUS,1000,2
4月,SUS,1100,3
"""

@st.cache_data
def load_quality_data(csv_text):
    time.sleep(2)

    df = pd.read_csv(StringIO(csv_text))
    df["ppm"] = (df["defects"] /df["production"] * 1000000).round(1)
    return df

st.title("品質データcsv読込キャッシュ確認アプリ")

st.write("""
このアプリでは、CSV風の品質データを読み込み、
ppmを計算して、拠点別にグラフ表示します。

@st.cache_data を使うことで、CSV読み込みやDataFrame変換の結果を覚え、
ボタン操作などで再実行されても、同じ処理を毎回やり直さないようにします
""")

df = load_quality_data(CSV_TEXT)
site_list = df["site"].unique()
selected_site = st.selectbox("確認する拠点を選んでください", site_list)

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
    st.error("注意レベル：高いです。すぐに内容が必要です。")
elif latest_ppm >= 3000:
    st.warning("注意レベル：やや高めです。傾向確認をおすすめします。")
else:
    st.success("注意レベル：低いです。大きな問題はなさそうです。")
