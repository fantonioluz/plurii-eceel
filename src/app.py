import streamlit as st
from db_utils import load_data_from_db
from analysis_utils import clean_balance_column, calculate_salary_expenses, calculate_monthly_profit
from visualization_utils import create_salary_chart, create_profit_chart
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

# Página "Análise por Banco"
if st.session_state.selected_page == "Análise por Banco":
    st.title("Análise por Banco")
    st.write("Aqui será o conteúdo da Análise por Banco.")

# Página "Histórico de Transações"
if st.session_state.selected_page == "Histórico de Transações":
    st.title("Histórico de Transações")
    st.write("Aqui será o histórico de transações.")
