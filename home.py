import os
import streamlit as st
import pandas as pd

from main_code import analyze_stocks_from_csv


def main():

    with st.sidebar:
        st.header("Evaluate Stocks", divider='blue')

        uploaded_file = st.file_uploader(
            "Upload Stock and Inital Price list:", type="csv")
        
        st.divider()

        stop_loss_percent = st.sidebar.number_input(
            "Stop Loss Percentage:", min_value=0.0, max_value=100.0, value=10.0)
        st.write("Desired stop loss percentage:", stop_loss_percent)

        st.divider()

        profit_target_percent = st.sidebar.number_input(
            "Profit Target Percentage:", min_value=0.0, max_value=100.0, value=15.0)
        st.write("Desired profit target percentage:", profit_target_percent)

        st.divider()
        with open(f"{os.getcwd()}/stock_prices.csv", "rb") as file:
            st.download_button("Download Sample file", data=file,
                               file_name="sample_stock_list.csv", mime="text/csv")

    if uploaded_file is not None:
        st.sidebar.success("File uploaded successfully!")
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
