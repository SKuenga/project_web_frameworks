import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import json
import os

def load_transaction(file): #This is used to Clean up the data before proceeding with the Analysis
    df = pd.read_csv(file)
    df["Amount"] = df["Amount"].str.replace(",", "", regex=False ).astype(float)
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)
    df = df.drop(columns=["Unnamed: 6"], axis = 1)
    with st.expander('Expand to see your transactions'):
        st.write(df)
    return df



st.set_page_config("Finance Automation")
def main():
    st.title("Finance Automation")
    uploaded_file = st.file_uploader("Upload your Bank_Statement", type = ["csv"])
    if uploaded_file is not None:
        df = load_transaction(uploaded_file)
        if df is not None:
            debit_df = df[df["Debit/Credit"] == "Debit"].copy()
            credit_df = df[df["Debit/Credit"] == "Credit"].copy()
            tab_1, tab_2 = st.tabs(["Expenses", "Payments"])
            with tab_1:
                st.write(debit_df)
            with tab_2:
                st.write(credit_df)
            with st.expander("Show summary Metrics"):
                st.title("Summary Metrics")
                st.subheader("Monthly Expenses")
                monthly_expense = df.resample("ME")["Amount"].sum()
                st.write(monthly_expense)
                #To show the total credits and total debits
                debit = debit_df["Amount"].sum()
                credit = credit_df["Amount"].sum()
                st.write(f"Debit: {debit} AED")
                st.write(f"Credit: {credit} AED")



main()