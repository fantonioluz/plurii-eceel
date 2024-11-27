import streamlit as st
from utils.visualization_utils import create_salary_chart, create_profit_chart
from utils.analysis_utils import clean_balance_column, calculate_salary_expenses, calculate_monthly_profit
from utils.db_utils import load_data_from_db


st.set_page_config(
    page_title="Dashboard Geral",
    page_icon="📊",  # Ícone de gráfico
    layout="wide"
)


st.title("Dashboard de Desempenho Financeiro")
# Carregar dados do banco
data = load_data_from_db()
# Limpar coluna 'saldo'
data = clean_balance_column(data)
# Gráfico de gastos mensais com funcionários
st.subheader("Gastos Mensais com Funcionários")
salary_expenses = calculate_salary_expenses(data)
salary_chart = create_salary_chart(salary_expenses)
st.altair_chart(salary_chart)
# Gráfico de lucro mensal
st.subheader("Lucro Mensal")
monthly_profit = calculate_monthly_profit(data)
profit_chart = create_profit_chart(monthly_profit)
st.altair_chart(profit_chart)