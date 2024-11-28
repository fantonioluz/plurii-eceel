import streamlit as st
import pandas as pd
from db_utils import load_data_from_db
from analysis_utils import (
    prepare_yearly_data_for_line_chart,
    prepare_monthly_data_for_line_chart,
    get_monthly_summary,
    get_yearly_summary,
    transform_data_for_display_in_table,
    convert_date_column,
    add_month_and_year_columns,
    clean_balance_column,
    calculate_salary_expenses,
    calculate_monthly_profit,
    prepare_account_data,
    prepare_credit_debit_data,
    prepare_profit_data,
    prepare_yearly_account_data,
    prepare_yearly_subaccount_data,
    comparar_calcular_total,
)
from visualization_utils import (
    create_yearly_line_chart,
    create_monthly_line_chart,
    create_monthly_summary_chart,
    create_yearly_summary_chart,
    create_credit_debit_chart,
    create_salary_chart,
    create_profit_chart,
    create_yearly_account_chart,
    create_yearly_subaccount_chart,
    comparar_semanal,
    comparar_mensal,
    comparar_anual,
)
from streamlit_option_menu import option_menu

st.markdown(
    """
    <style>
    .stMainBlockContainer.block-container {
        max-width: 1200px; /* Altere para o tamanho desejado */
        padding: 2rem; /* Ajuste o espaçamento interno */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Inicializar o estado da página
if "selected_page" not in st.session_state:
    st.session_state.selected_page = "Início"

# Sidebar com menu
with st.sidebar:
    selected = option_menu(
        "FinancePro",
        ["Início", "Dashboard Geral", "Análise por Banco", "Histórico de Transações"],
        icons=["house", "bar-chart-line", "graph-up", "clock-history"],
        menu_icon="cast",
        default_index=[
            "Início",
            "Dashboard Geral",
            "Análise por Banco",
            "Histórico de Transações",
        ].index(st.session_state.selected_page),
    )

# Atualizar a página com base no menu selecionado
if selected != st.session_state.selected_page:
    st.session_state.selected_page = selected

# Página "Início"
if st.session_state.selected_page == "Início":
    # Cabeçalho principal
    st.title("ECEEL - TEC")
    st.markdown("### Olá, Mª Helena!")
    st.write(
        "Seja bem-vinda à sua área exclusiva de organização financeira, explore e impulsione seu negócio."
    )

    # Imagem da usuária
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(
            "src/images/Mask group.png", width=150, caption="Gestora"
        )  # Ajuste o caminho, se necessário
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
    if period_type == "Anual":
        num_periods = st.slider(
            "Quantos anos você deseja visualizar?", min_value=1, max_value=3, value=3
        )
    else:
        num_periods = st.slider(
            "Quantos períodos você deseja visualizar?",
            min_value=1,
            max_value=12,
            value=3,
        )

    # Calcular totais
    totais_semana, totais_mes, totais_ano = comparar_calcular_total(data)

    # Mostrar os dados e gráficos com base na seleção
    if period_type == "Semanal":
        st.markdown(f"#### Últimas {num_periods} semanas")
        weekly_data = totais_semana.head(num_periods)
        fig_semana = comparar_semanal(weekly_data)
        st.plotly_chart(fig_semana)
        st.write("Dados detalhados das semanas selecionadas:")
        st.dataframe(weekly_data)

    elif period_type == "Mensal":
        st.markdown(f"#### Últimos {num_periods} meses")
        monthly_data = totais_mes.head(num_periods)
        fig_mes = comparar_mensal(monthly_data)
        st.plotly_chart(fig_mes)
        st.write("Dados detalhados dos meses selecionados:")
        st.dataframe(monthly_data)

    elif period_type == "Anual":
        st.markdown(f"#### Últimos {num_periods} anos")
        yearly_data = totais_ano.head(num_periods)
        fig_ano = comparar_anual(yearly_data)
        st.plotly_chart(fig_ano)
        st.write("Dados detalhados dos anos selecionados:")
        st.dataframe(yearly_data)

# Página "Análise por Banco"
if st.session_state.selected_page == "Análise por Banco":
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


# Página "Histórico de Transações"
if st.session_state.selected_page == "Histórico de Transações":
    st.title("Histórico de Transações")

    data = load_data_from_db()
    data = convert_date_column(data, "data")

    col1, col2, col6, col7, col8 = st.columns(5)
    with col1:
        selected_month = st.selectbox(
            "Selecione o mês", ["Ano Todo"] + [f"{i:02d}" for i in range(1, 13)]
        )
    with col2:
        selected_year = st.number_input(
            "Digite o ano",
            min_value=2000,
            max_value=int(pd.Timestamp.now().year),
            value=int(pd.Timestamp.now().year),
            step=1,
        )

    if selected_month == "Ano Todo":
        filtered_data = data[data["data"].dt.year == selected_year]
    else:
        filtered_data = data[
            (data["data"].dt.month == int(selected_month))
            & (data["data"].dt.year == selected_year)
        ]
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
            unique_subaccounts = transformed_data["subconta"].unique()
            selected_subaccount = st.selectbox(
                "Selecione a Subconta", options=["Todas"] + list(unique_subaccounts)
            )
            if selected_subaccount != "Todas":
                transformed_data = transformed_data[
                    transformed_data["subconta"] == selected_subaccount
                ]
        with col8:
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
            st.dataframe(transformed_data[columns_to_display].reset_index(drop=True))

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
