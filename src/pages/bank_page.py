import altair as alt
import streamlit as st
import pandas as pd
from utils.analysis_utils import clean_balance_column, calculate_salary_expenses, calculate_monthly_profit, analyze_bank_transactions, analyze_for_bank
from utils.visualization_utils import create_salary_chart, create_profit_chart, create_bank_analysis_chart, create_for_one_bank_chart
from utils.db_utils import load_data_from_db


st.set_page_config(
    page_title="Análise por Banco",
    page_icon="🏦",  # Ícone de banco
    layout="wide"
)

st.title("Análise por Banco")

# Carregar dados do banco
data = load_data_from_db()

# Limpar coluna 'saldo'
data = clean_balance_column(data)

# Converter coluna 'data' para datetime
data['data'] = pd.to_datetime(data['data'], errors='coerce')

# Filtros de data
st.write("### Filtros")
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Data Inicial", value=data['data'].min().date())
with col2:
    end_date = st.date_input("Data Final", value=data['data'].max().date())

# Converter datas para datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filtrar dados pelo intervalo de datas
filtered_data = data[(data['data'] >= start_date) & (data['data'] <= end_date)]

# Seleção de banco
st.write("### Selecione o Banco")
bancos_disponiveis = filtered_data['banco'].unique()
banco_selecionado = st.selectbox("Banco", options=bancos_disponiveis)

# Filtrar dados pelo banco selecionado
banco_data = filtered_data[filtered_data['banco'] == banco_selecionado]

banco_analysis = analyze_for_bank(banco_data)

# Gráfico de análise mês a mês
st.write(f"### Gráfico de Entradas e Saídas Mensais: {banco_selecionado}")
banco_chart = create_for_one_bank_chart(banco_analysis, banco_selecionado)
st.altair_chart(banco_chart)
st.write("### Geral Bancos")

bank_general_analysis = analyze_bank_transactions(filtered_data, start_date, end_date)

bank_general_visualization = create_bank_analysis_chart(bank_general_analysis)
st.altair_chart(bank_general_visualization)