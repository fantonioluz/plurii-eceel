import streamlit as st
import pandas as pd
from utils.analysis_utils import convert_date_column, transform_data_for_display_in_table

from utils.db_utils import load_data_from_db

st.title("Histórico de Transações")
data = load_data_from_db()
data = convert_date_column(data, "data")
col1, col2, col6, col7, col8, col9 = st.columns(6)
with col1:
    selected_month = st.selectbox(
        "Selecione o mês", ["Ano Todo"] + [f"{i:02d}" for i in range(1, 13)]
    )
with col2:
    # Define os anos disponíveis no seletor
    available_years = ["Todos os Anos", 2022, 2023, 2024]
    selected_year = st.selectbox("Selecione o Ano", options=available_years)

if selected_month == "Ano Todo":
    filtered_data = data[data["data"].dt.year == selected_year]
else:
    filtered_data = data[
        (data["data"].dt.month == int(selected_month))
        & (data["data"].dt.year == selected_year)
    ]

if selected_year != "Todos os Anos":
    filtered_data = data[data["data"].dt.year == int(selected_year)]
else:
    filtered_data = data

transformed_data = transform_data_for_display_in_table(filtered_data)
if transformed_data.empty:
    st.warning("Nenhum dado encontrado para o período selecionado.")
else:
    # Filtros
    with col6:
        unique_banks = transformed_data["banco"].unique()
        selected_bank = st.selectbox(
            "Selecione o Banco", options=["Todos"] + list(unique_banks)
        )
        if selected_bank != "Todos":
            transformed_data = transformed_data[
                transformed_data["banco"] == selected_bank
            ]
    
    with col7: 
        unique_accounts = transformed_data["conta"].unique()
        selected_account = st.selectbox(
            "Selecione a Conta", options=["Todas"] + list(unique_accounts)
        )
        if selected_account != "Todas":
            transformed_data = transformed_data[
                transformed_data["conta"] == selected_account
            ]
    with col8:
            unique_subaccounts = transformed_data["subconta"].unique()
            selected_subaccount = st.selectbox(
                "Selecione a Subconta", options=["Todas"] + list(unique_subaccounts)
            )
            if selected_subaccount != "Todas":
                transformed_data = transformed_data[
                    transformed_data["subconta"] == selected_subaccount
                ]
    with col9:
        description_filter = st.text_input("Filtrar por Descrição")
        if description_filter:
            transformed_data = transformed_data[
                transformed_data["descricao"].str.contains(
                    description_filter, case=False, na=False
                )
            ]
    if transformed_data.empty:
        st.warning("Nenhum dado encontrado com os filtros aplicados.")
    else:
        columns_to_display = [
            "data",
            "descricao",
            "documento",
            "valor",
            "banco",
            "conta",
            "subconta",
        ]
        st.dataframe(transformed_data[columns_to_display].reset_index(drop=True), use_container_width=True)
    total_debit = transformed_data["debito"].sum()
    total_credit = transformed_data["credito"].sum()
    total_profit = total_credit - total_debit
    col3, col4, col5 = st.columns(3)
    with col3:
        st.markdown(
            f"""
            <div style="
                background-color: #e7f9e7;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                font-size: 16px;
                font-weight: bold;
                color: #4CAF50; 
                margin: 30px;
            ">
            Total Crédito: R$ {total_credit:,.2f}
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            f"""
            <div style="
                background-color: #f9e7e7;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                font-size: 16px;
                font-weight: bold;
                color: #FF5733;
                margin: 30px;
            ">
            Total Débito: R$ {total_debit:,.2f}
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col5:
        st.markdown(
            f"""
            <div style="
                background-color: #e7f3f9;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                font-size: 16px;
                font-weight: bold;
                color: #33B5E5;
                margin: 30px;
            ">
            Total Lucro: R$ {total_profit:,.2f}
            </div>
            """,
            unsafe_allow_html=True,
        )
