import streamlit as st
from utils.analysis_utils import (
    analyze_supplier_profitability, clean_balance_column, calculate_salary_expenses, calculate_monthly_profit,
    prepare_credit_debit_data, prepare_yearly_account_data, prepare_yearly_subaccount_data,
    comparar_calcular_total
)
from utils.visualization_utils import (
    create_salary_chart, create_profit_chart, create_credit_debit_chart, create_supplier_profit_chart,
    create_yearly_account_chart, create_yearly_subaccount_chart
)
from utils.db_utils import load_data_from_db
import pandas as pd

st.title("Dashboard de Desempenho Financeiro")

# Carregar dados do banco
data = load_data_from_db()
data = clean_balance_column(data)

# Converter coluna de data
data['data'] = pd.to_datetime(data['data'])
data['year'] = data['data'].dt.year

# Filtro de intervalo de anos
st.sidebar.header("Filtros")
available_years = sorted(data['year'].unique())
start_year, end_year = st.sidebar.select_slider(
    "Selecione o intervalo de anos:",
    options=available_years,
    value=(min(available_years), max(available_years))
)

# Filtrar dados pelo intervalo de anos
filtered_data = data[(data['year'] >= start_year) & (data['year'] <= end_year)]

# Mensagem informativa
if filtered_data.empty:
    st.warning("Não há dados para o intervalo de anos selecionado.")
else:
    # Organizar os gráficos em abas
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Geral", "📈 Entradas e Saídas", "🏦 Contas e Subcontas", "🔮 Guru das Previsões", "🚚 Fornecedores"])

    # Aba: Geral
    with tab1:
        st.markdown("### Análises Gerais")
        col1, col2 = st.columns(2)
        with col1:
            # Gráfico de gastos com funcionários
            salary_expenses = calculate_salary_expenses(filtered_data)
            if not salary_expenses.empty:
                st.markdown("#### Gastos Mensais com Funcionários")
                salary_chart = create_salary_chart(salary_expenses)
                st.altair_chart(salary_chart, use_container_width=True)
            else:
                st.info("Sem dados de gastos com funcionários para o período.")

        with col2:
            # Gráfico de lucro mensal
            monthly_profit = calculate_monthly_profit(filtered_data)
            if not monthly_profit.empty:
                st.markdown("#### Lucro Mensal")
                profit_chart = create_profit_chart(monthly_profit)
                st.altair_chart(profit_chart, use_container_width=True)
            else:
                st.info("Sem dados de lucro mensal para o período.")

    # Aba: Entradas e Saídas
    with tab2:
        st.markdown("### Entradas e Saídas Mensais")
        credit_debit_data = prepare_credit_debit_data(filtered_data)
        if not credit_debit_data.empty:
            credit_debit_chart = create_credit_debit_chart(credit_debit_data)
            st.altair_chart(credit_debit_chart, use_container_width=True)
        else:
            st.info("Sem dados de entradas e saídas para o período.")

# Aba: Contas e Subcontas
    with tab3:
        st.markdown("### Total de Débito e Crédito por Ano e Conta/Subconta")

        # Filtro para selecionar o tipo de conta
        available_accounts = filtered_data['conta'].unique()
        selected_account = st.selectbox("Selecione o tipo de conta:", options=available_accounts, index=0)

        # Filtrar os dados pelo tipo de conta selecionado
        filtered_account_data = filtered_data[filtered_data['conta'] == selected_account]

        if filtered_account_data.empty:
            st.info(f"Não há dados para a conta '{selected_account}' no período selecionado.")
        else:
            # Filtro para selecionar o tipo de subconta
            available_subaccounts = filtered_account_data['subconta'].unique()
            selected_subaccount = st.selectbox("Selecione o tipo de subconta:", options=available_subaccounts, index=0)

            # Filtrar os dados pelo tipo de subconta selecionado
            filtered_subaccount_data = filtered_account_data[filtered_account_data['subconta'] == selected_subaccount]

            if filtered_subaccount_data.empty:
                st.info(f"Não há dados para a subconta '{selected_subaccount}' no período selecionado.")
            else:
                # Gráficos por ano e conta/subconta
                col1, col2 = st.columns(2)

                with col1:
                    yearly_account_data = prepare_yearly_account_data(filtered_subaccount_data)
                    if not yearly_account_data.empty:
                        st.markdown(f"#### Por Ano e Conta: {selected_account}")
                        yearly_account_chart = create_yearly_account_chart(yearly_account_data)
                        st.altair_chart(yearly_account_chart, use_container_width=True)
                    else:
                        st.info("Sem dados de contas para o período selecionado.")

                with col2:
                    yearly_subaccount_data = prepare_yearly_subaccount_data(filtered_subaccount_data, selected_subaccount)
                    if not yearly_subaccount_data.empty:
                        st.markdown(f"#### Por Subconta: {selected_subaccount}")
                        yearly_subaccount_chart = create_yearly_subaccount_chart(yearly_subaccount_data, selected_subaccount)
                        st.altair_chart(yearly_subaccount_chart, use_container_width=True)
                    else:
                        st.info("Sem dados de subcontas para o período selecionado.")
    with tab4:
        
        st.markdown("### Previsões")
        
    with tab5:
        st.markdown("### Fornecedores")
        # Filtrar os dados pelo intervalo de tempo selecionado
        filtered_data = data[(data['year'] >= start_year) & (data['year'] <= end_year)]
        
        # Realizar a análise de rentabilidade
        profitability = analyze_supplier_profitability(filtered_data)
        
        if profitability.empty:
            st.warning("Não há dados suficientes para calcular a rentabilidade dos fornecedores no período selecionado.")
        else:
            # Exibir a tabela de rentabilidade
            st.markdown("### Rentabilidade por Fornecedor")
            st.dataframe(profitability, use_container_width=True)
        
            # Criar e exibir o gráfico de rentabilidade
            supplier_profit_chart = create_supplier_profit_chart(profitability)
            st.altair_chart(supplier_profit_chart, use_container_width=True)


