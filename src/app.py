import streamlit as st
from db_utils import load_data_from_db
from analysis_utils import clean_balance_column, calculate_salary_expenses, calculate_monthly_profit, prepare_account_data, prepare_credit_debit_data, prepare_profit_data, prepare_yearly_account_data, prepare_yearly_subaccount_data
from visualization_utils import create_account_chart, create_credit_debit_chart,  create_salary_chart, create_profit_chart, create_yearly_account_chart, create_yearly_subaccount_chart
from streamlit_option_menu import option_menu

# Inicializar o estado da página
if "selected_page" not in st.session_state:
    st.session_state.selected_page = "Início"

# Sidebar com menu
with st.sidebar:
    selected = option_menu(
        "FinancePro",
        ["Início", "Dashboard Geral", "Análise por Banco", "Histórico de Transações"],
        icons=['house', 'bar-chart-line', 'graph-up', 'clock-history'],
        menu_icon="cast",
        default_index=["Início", "Dashboard Geral", "Análise por Banco", "Histórico de Transações"].index(st.session_state.selected_page)
    )

# Atualizar a página com base no menu selecionado
if selected != st.session_state.selected_page:
    st.session_state.selected_page = selected

# Página "Início"
if st.session_state.selected_page == "Início":
    # Cabeçalho principal
    st.title("ECEEL - TEC")
    st.markdown("### Olá, Mª Helena!")
    st.write("Seja bem-vinda à sua área exclusiva de organização financeira, explore e impulsione seu negócio.")
    
    # Imagem da usuária
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("src/images/Mask group.png", width=150, caption="Gestora")  # Ajuste o caminho, se necessário
    with col2:
        st.write("### Mª Helena de Souza")
        st.write("**Status:** Nenhuma notificação no momento")
    
    # Notificações
    st.info("🔔 Não há nenhuma notificação no momento.")
    
    # Botões de navegação
    st.write("### Ações rápidas")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Ir ao Dashboard"):
            st.session_state.selected_page = "Dashboard Geral"
            st.query_params.update(page="Dashboard Geral")  # Redirecionar
    with col2:
        if st.button("Histórico de Transações"):
            st.session_state.selected_page = "Histórico de Transações"
            st.query_params.update(page="Histórico de Transações")  # Redirecionar

# Página "Dashboard Geral"
if st.session_state.selected_page == "Dashboard Geral":
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
    yearly_subaccount_data_pessoal = prepare_yearly_subaccount_data(data, 'Despesa com pessoal')
    yearly_subaccount_chart_pessoal = create_yearly_subaccount_chart(yearly_subaccount_data_pessoal, 'Despesa com pessoal')
    st.altair_chart(yearly_subaccount_chart_pessoal)

    # Gráfico de total de débito e crédito por ano e subconta para 'Despesas administrativas'
    st.subheader("Total de Débito e Crédito por Ano e Subconta (Despesas administrativas)")
    yearly_subaccount_data_administrativas = prepare_yearly_subaccount_data(data, 'Despesas administrativas')
    yearly_subaccount_chart_administrativas = create_yearly_subaccount_chart(yearly_subaccount_data_administrativas, 'Despesas administrativas')
    st.altair_chart(yearly_subaccount_chart_administrativas)
 
# Página "Análise por Banco"
if st.session_state.selected_page == "Análise por Banco":
    st.title("Análise por Banco")
    st.write("Aqui será o conteúdo da Análise por Banco.")

# Página "Histórico de Transações"
if st.session_state.selected_page == "Histórico de Transações":
    st.title("Histórico de Transações")
    st.write("Aqui será o histórico de transações.")
