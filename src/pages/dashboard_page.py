import streamlit as st
from utils.visualization_utils import create_salary_chart, create_profit_chart, create_credit_debit_chart, create_yearly_account_chart, create_yearly_subaccount_chart, comparar_semanal, comparar_mensal, comparar_anual
from utils.analysis_utils import clean_balance_column, calculate_salary_expenses, calculate_monthly_profit, prepare_credit_debit_data, prepare_yearly_account_data, prepare_yearly_subaccount_data, comparar_calcular_total
from utils.db_utils import load_data_from_db





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

# Preparar dados para entradas e saídas mensais
credit_debit_data = prepare_credit_debit_data(data)

# Gráfico de entradas e saídas mensais
st.subheader("Entradas e Saídas Mensais (Crédito e Débito)")
credit_debit_chart = create_credit_debit_chart(credit_debit_data)
st.altair_chart(credit_debit_chart)

# Exibir tabela de dados de entradas e saídas mensais
st.write("Dados de Entradas e Saídas Mensais:")
st.write(credit_debit_data)
# Gráfico de total de débito e crédito por ano e conta
st.subheader("Total de Débito e Crédito por Ano e Conta")
yearly_account_data = prepare_yearly_account_data(data)
yearly_account_chart = create_yearly_account_chart(yearly_account_data)
st.altair_chart(yearly_account_chart)

# Gráfico de total de débito e crédito por ano e subconta para 'Despesa com pessoal'
st.subheader("Total de Débito e Crédito por Ano e Subconta (Despesa com pessoal)")
yearly_subaccount_data_pessoal = prepare_yearly_subaccount_data(
    data, "Despesa com pessoal"
)
yearly_subaccount_chart_pessoal = create_yearly_subaccount_chart(
    yearly_subaccount_data_pessoal, "Despesa com pessoal"
)
st.altair_chart(yearly_subaccount_chart_pessoal)
# Gráfico de total de débito e crédito por ano e subconta para 'Despesas administrativas'
st.subheader(
    "Total de Débito e Crédito por Ano e Subconta (Despesas administrativas)"
)
yearly_subaccount_data_administrativas = prepare_yearly_subaccount_data(
    data, "Despesas administrativas"
)
yearly_subaccount_chart_administrativas = create_yearly_subaccount_chart(
    yearly_subaccount_data_administrativas, "Despesas administrativas"
)
st.altair_chart(yearly_subaccount_chart_administrativas)
# Comparação de ganhos e gastos
st.subheader("Comparação de Ganhos e Gastos")
# Selecionar o tipo de período
period_type = st.radio(
    "Selecione o tipo de período para análise:", ["Semanal", "Mensal", "Anual"]
)
# Controlar o número de períodos a exibir
num_periods = st.slider(
    "Quantos períodos você deseja visualizar?",
    min_value=1,
    max_value=3,
    value=3
)
# Calcular totais
totais_semana, totais_mes, totais_ano = comparar_calcular_total(data)
# Mostrar os dados e gráficos com base na seleção
if period_type == "Semanal":
    st.markdown(f"#### Últimas {num_periods} semanas")
    weekly_data = totais_semana.head(num_periods)
    chart_semanal = comparar_semanal(weekly_data)
    st.altair_chart(chart_semanal, use_container_width=True)
    st.write("Dados detalhados das semanas selecionadas:")
    st.dataframe(weekly_data)
elif period_type == "Mensal":
    st.markdown(f"#### Últimos {num_periods} meses")
    monthly_data = totais_mes.head(num_periods)
    chart_mensal = comparar_mensal(monthly_data)
    st.altair_chart(chart_mensal, use_container_width=True)
    st.write("Dados detalhados dos meses selecionados:")
    st.dataframe(monthly_data)
elif period_type == "Anual":
    st.markdown(f"#### Últimos {num_periods} anos")
    yearly_data = totais_ano.head(num_periods)
    chart_anual = comparar_anual(yearly_data)
    st.altair_chart(chart_anual, use_container_width=True)
    st.write("Dados detalhados dos anos selecionados:")
    st.dataframe(yearly_data)