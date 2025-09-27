from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st


st.set_page_config(page_title="データ可視化ダッシュボード", layout="wide")


def initialize_session_state():
    if "user_inputs" not in st.session_state:
        st.session_state.user_inputs = {
            "name": "ゲスト",
            "age": 30,
            "interest": "データサイエンス",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }


def update_session_state(name: str, age: int, interest: str):
    st.session_state.user_inputs.update(
        {
            "name": name,
            "age": age,
            "interest": interest,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )


def sidebar_inputs():
    st.sidebar.header("ユーザー設定")
    name = st.sidebar.text_input("名前", value=st.session_state.user_inputs["name"])
    age = st.sidebar.number_input(
        "年齢", min_value=0, max_value=120, value=st.session_state.user_inputs["age"], step=1
    )
    interest_options = ["データサイエンス", "機械学習", "Web開発", "可視化", "ビジネス分析"]
    try:
        default_index = interest_options.index(st.session_state.user_inputs["interest"])
    except ValueError:
        default_index = 0
    interest = st.sidebar.selectbox(
        "関心領域",
        options=interest_options,
        index=default_index,
    )
    if st.sidebar.button("セッション更新"):
        update_session_state(name, int(age), interest)
        st.sidebar.success("セッション情報を更新しました！")


def generate_sample_data():
    dates = pd.date_range(datetime.now().date(), periods=30)
    data = pd.DataFrame(
        {
            "date": dates,
            "value": np.random.randint(50, 150, size=len(dates)),
            "category": np.random.choice(["A", "B", "C"], size=len(dates)),
        }
    )
    return data


def render_charts(data: pd.DataFrame):
    st.subheader("時系列ラインチャート (Streamlit)")
    line_chart_data = (
        data.pivot_table(index="date", columns="category", values="value", aggfunc="mean")
        .sort_index()
    )
    st.line_chart(line_chart_data, use_container_width=True)

    st.subheader("カテゴリ別バーチャート (Streamlit)")
    category_means = data.groupby("category")["value"].mean().sort_index()
    st.bar_chart(category_means, use_container_width=True)


def render_map():
    st.subheader("位置情報マップ")
    map_data = pd.DataFrame(
        {
            "lat": [35.6804, 34.6937, 35.0116],
            "lon": [139.7690, 135.5022, 135.7681],
            "city": ["東京", "大阪", "京都"],
        }
    )
    st.map(map_data, zoom=5)


def render_table(data: pd.DataFrame):
    st.subheader("データプレビュー")
    st.dataframe(data.head(10))


def render_image():
    st.subheader("イメージギャラリー")
    gradient = np.linspace(0, 1, 256)
    gradient = np.tile(gradient, (256, 1))
    colored_image = np.dstack((gradient, gradient[::-1], np.ones_like(gradient)))
    st.image(colored_image, caption="NumPy で生成したグラデーション画像", use_column_width=True)


def render_session_state_summary():
    st.subheader("セッション情報")
    st.json(st.session_state.user_inputs)


def render_file_uploader():
    st.subheader("CSV ファイルアップロード")
    uploaded_file = st.file_uploader("CSV ファイルを選択", type="csv")
    if uploaded_file is not None:
        try:
            uploaded_df = pd.read_csv(uploaded_file)
            st.success("ファイルを読み込みました")
            st.dataframe(uploaded_df)
        except Exception as error:  # pylint: disable=broad-except
            st.error(f"CSV の読み込みに失敗しました: {error}")


def render_summary_metrics(data: pd.DataFrame):
    st.subheader("主要指標")
    col1, col2, col3 = st.columns(3)
    col1.metric("データ件数", len(data))
    col2.metric("平均値", f"{data['value'].mean():.1f}")
    col3.metric("最大値", int(data['value'].max()))


def render_layout():
    st.title("Streamlit データダッシュボード")
    st.caption("サイドバーからパラメータを調整し、可視化やデータを探索してください。")

    data = generate_sample_data()

    render_summary_metrics(data)

    chart_col, table_col = st.columns((2, 1))
    with chart_col:
        render_charts(data)
        render_map()
    with table_col:
        render_table(data)
        render_image()

    render_file_uploader()
    render_session_state_summary()


def main():
    initialize_session_state()
    sidebar_inputs()
    render_layout()


if __name__ == "__main__":
    main()
