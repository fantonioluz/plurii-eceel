import altair as alt
import streamlit as st
import pandas as pd
from utils.analysis_utils import get_yearly_summary, get_monthly_summary, prepare_yearly_data_for_line_chart, prepare_monthly_data_for_line_chart, convert_date_column, add_month_and_year_columns
from utils.visualization_utils import create_yearly_summary_chart, create_yearly_line_chart, create_monthly_summary_chart, create_monthly_line_chart
from utils.db_utils import load_data_from_db



st.title("Análise por Banco e Ano")
data = load_data_from_db()
data = convert_date_column(data, "data")
data = add_month_and_year_columns(data, "data")

# Filtros
col1, col2, col3 = st.columns(3)
with col1:
    bancos_disponiveis = ["Todos os Bancos"] + list(data["banco"].unique())
    selected_bank = st.selectbox("Selecione o Banco", bancos_disponiveis)

with col2:
    anos_disponiveis = ["Todos os Anos"] + sorted(data["data"].dt.year.unique())
    selected_year = st.selectbox("Selecione o Ano", anos_disponiveis)

with col3:
    chart_type = st.radio("Selecione o Tipo de Gráfico", ["Barra", "Linha"])

if selected_bank != "Todos os Bancos":
    data = data[data["banco"] == selected_bank]

if selected_year != "Todos os Anos":
    data = data[data["data"].dt.year == selected_year]

data["ano"] = data["data"].dt.year
if chart_type == "Barra":
    credit_summary = get_yearly_summary(data, "credito")
    debit_summary = get_yearly_summary(data, "debito")
    credit_chart = create_yearly_summary_chart(
        credit_summary, "credito", title="Resumo Anual de Crédito"
    )
    debit_chart = create_yearly_summary_chart(
        debit_summary, "debito", title="Resumo Anual de Débito"
    )
else:
    credit_summary = prepare_yearly_data_for_line_chart(data, "credito")
    debit_summary = prepare_yearly_data_for_line_chart(data, "debito")
    credit_chart = create_yearly_line_chart(
        credit_summary, "credito", title="Crédito Anual por Banco"
    )
    debit_chart = create_yearly_line_chart(
        debit_summary, "debito", title="Débito Anual por Banco"
    )

st.subheader("Gráficos de Crédito e Débito")
col4, col5 = st.columns(2)
with col4:
    st.altair_chart(credit_chart, use_container_width=True)
with col5:
    st.altair_chart(debit_chart, use_container_width=True)

if chart_type == "Barra":
    credit_summary_month = get_monthly_summary(data, "credito")
    debit_summary_month = get_monthly_summary(data, "debito")
    credit_chart_month = create_monthly_summary_chart(
        credit_summary_month, "credito", title="Resumo Mensal de Crédito"
    )
    debit_chart_month = create_monthly_summary_chart(
        debit_summary_month, "debito", title="Resumo Mensal de Débito"
    )
else:
    # gráficos de linha
    credit_summary_month = prepare_monthly_data_for_line_chart(data, "credito")
    debit_summary_month = prepare_monthly_data_for_line_chart(data, "debito")
    credit_chart_month = create_monthly_line_chart(
        credit_summary_month, "credito", title="Crédito Mensal por Banco"
    )
    debit_chart_month = create_monthly_line_chart(
        debit_summary_month, "debito", title="Débito Mensal por Banco"
    )

st.subheader("Gráficos de Crédito e Débito por Mês")
col6, col7 = st.columns(2)
with col6:
    st.altair_chart(credit_chart_month, use_container_width=True)
with col7:
    st.altair_chart(debit_chart_month, use_container_width=True)
