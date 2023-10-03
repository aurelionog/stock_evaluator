import streamlit as st
import pandas as pd
from io import StringIO

from main_code import analyze_stocks_from_csv


def main():

    with st.sidebar:
        st.header("Evaluate Stocks", divider='blue')

        uploaded_file = st.file_uploader(
            "Upload Stock and Inital Price list:", type="csv")

        st.divider()

        stop_loss_percent = st.slider(
            "Set your desired stop-loss percentage", 1, 50, 10)
        st.write("Stop-loss percentage:", stop_loss_percent)

        st.divider()

        profit_target_percent = st.slider(
            "Set your desired profit target percentage", 1, 100, 15)
        st.write("Desired profit target percentage:", profit_target_percent)

    if uploaded_file is not None:
        dataframe = pd.read_csv(uploaded_file)

        analysis_df = analyze_stocks_from_csv(
            dataframe, stop_loss_percent, profit_target_percent)

        st.title('Result:')
        analysis_df


if __name__ == "__main__":
    st.set_page_config(
        page_title="Evaluate Stocks", page_icon=":chart_with_upwards_trend:"
    )
    main()
