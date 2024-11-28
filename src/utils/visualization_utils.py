import altair as alt

def create_salary_chart(salary_expenses):
    """
    Cria um gráfico de barras para gastos mensais com funcionários.
    """
    return alt.Chart(salary_expenses).mark_bar().encode(
        x=alt.X('Mês:O', title='Mês', sort=None),
        y=alt.Y('Gastos com Funcionários:Q', title='Gastos (R$)'),
        tooltip=[alt.Tooltip('Mês:O', title='Mês'), alt.Tooltip('Gastos com Funcionários:Q', title='Gastos (R$)', format='.2f')]
    ).properties(
        width=800,
        height=400
        
    )

def create_profit_chart(monthly_profit):
    """
    Cria um gráfico de linha para lucro mensal.
    """
    return alt.Chart(monthly_profit).mark_line(point=True).encode(
        x=alt.X('Mês:O', title='Mês', sort=None),
        y=alt.Y('Lucro:Q', title='Lucro (R$)', scale=alt.Scale(domain=(monthly_profit['Lucro'].min(), monthly_profit['Lucro'].max()))),
        tooltip=[alt.Tooltip('Mês:O', title='Mês'), alt.Tooltip('Lucro:Q', title='Lucro (R$)', format='.2f')]
    ).properties(
        width=800,
        height=400
        
    )


def create_bank_analysis_chart(bank_data):
    """
    Cria um gráfico de barras para entradas e saídas por banco.
    """
    chart = alt.Chart(bank_data).mark_bar().encode(
        x=alt.X('banco:O', title='Banco'),
        y=alt.Y('Valor:Q', title='Valor (R$)'),
        color='Tipo:N',
        tooltip=['banco', 'Tipo', 'Valor']
    ).properties(
        width=800,
        height=400,
        title="Entradas e Saídas por Banco"
    )
    return chart

def create_for_one_bank_chart(banco_analysis, banco_selecionado):
    banco_analysis['Mês'] = banco_analysis['data'].dt.to_period('M').astype(str)  # Agrupar por mês
    banco_chart = alt.Chart(banco_analysis).mark_bar().encode(
        x=alt.X('Mês:O', title='Mês', sort=None),
        y=alt.Y('Valor:Q', title='Valor (R$)'),
        color='Tipo:N',
        tooltip=['Mês', 'Tipo', 'Valor']
    ).properties(
        width=800,
        height=400,
        title=f"Entradas e Saídas Mensais - {banco_selecionado}"
    )
    return banco_chart


def create_credit_debit_chart(grouped):
    """
    Cria um gráfico de barras para entradas e saídas (Crédito e Débito) mensais lado a lado.
    """
    chart = (
        alt.Chart(grouped)
        .transform_fold(["credito", "debito"], as_=["Tipo", "Valor"])
        .mark_bar()
        .encode(
            x=alt.X("year_month:O", title="Mês"),
            y=alt.Y("Valor:Q", title="Valor (R$)"),
            color="Tipo:N",
            xOffset="Tipo:N",
            tooltip=[
                alt.Tooltip("year_month:O", title="Mês"),
                alt.Tooltip("Valor:Q", title="Valor (R$)", format=".2f"),
            ],
        )
        .properties(
            width=800, height=400, title="Entradas e Saídas Mensais (Crédito e Débito)"
        )
        .configure_axis(labelFontSize=12, titleFontSize=14)
        .configure_title(fontSize=16)
    )

    return chart


def create_account_chart(grouped_conta):
    """
    Cria um gráfico de barras para entradas e saídas por conta.
    """
    return (
        alt.Chart(grouped_conta)
        .transform_fold(["credito", "debito"], as_=["Tipo", "Valor"])
        .mark_bar()
        .encode(
            x=alt.X("conta:O", title="Conta"),
            y=alt.Y("Valor:Q", title="Valor (R$)"),
            color="Tipo:N",
            tooltip=[
                alt.Tooltip("conta:O", title="Conta"),
                alt.Tooltip("Valor:Q", title="Valor (R$)", format=".2f"),
            ],
        )
        .properties(
            width=800,
            height=400,
            title="Entradas e Saídas por Conta (Crédito e Débito)",
        )
    )
    
def create_yearly_account_chart(grouped):
    """
    Cria um gráfico de barras para total de débito e crédito por ano e conta.
    """
    chart = (
        alt.Chart(grouped)
        .transform_fold(["credito", "debito"], as_=["Tipo", "Valor"])
        .mark_bar()
        .encode(
            x=alt.X("year:O", title="Ano"),
            y=alt.Y("Valor:Q", title="Valor (R$)"),
            color="Tipo:N",
            column="conta:N",
            tooltip=[
                alt.Tooltip("year:O", title="Ano"),
                alt.Tooltip("Valor:Q", title="Valor (R$)", format=".2f"),
            ],
        )
        .properties(
            width=150, height=400, title="Total de Débito e Crédito por Ano e Conta"
        )
        .configure_axis(labelFontSize=12, titleFontSize=14)
        .configure_title(fontSize=16)
    )

    return chart

def create_yearly_subaccount_chart(grouped, conta):
    """
    Cria um gráfico de barras para total de débito e crédito por ano e subconta para uma conta específica.
    """
    # Ordenar subcontas por maior despesa (débito) dentro de cada ano
    sorted_grouped = grouped.sort_values(by=["year", "debito"], ascending=[True, False])

    chart = (
        alt.Chart(sorted_grouped)
        .transform_fold(["credito", "debito"], as_=["Tipo", "Valor"])
        .mark_bar()
        .encode(
            x=alt.X("year:O", title="Ano"),
            y=alt.Y("Valor:Q", title="Valor (R$)"),
            color="Tipo:N",
            column="subconta:N",
            tooltip=[
                alt.Tooltip("year:O", title="Ano"),
                alt.Tooltip("Valor:Q", title="Valor (R$)", format=".2f"),
            ],
        )
        .properties(
            width=150,
            height=400,
            title=f"Total de Débito e Crédito por Ano e Subconta ({conta})",
        )
        .configure_axis(labelFontSize=12, titleFontSize=14)
        .configure_title(fontSize=16)
    )

    return chart


def create_yearly_summary_chart(yearly_data, value_column, title="Resumo Anual"):
    """
    Cria um gráfico de barras ou linhas para resumir valores por ano.
    """
    chart = (
        alt.Chart(yearly_data)
        .mark_bar()
        .encode(
            x=alt.X("ano:O", title="Ano"),
            y=alt.Y(
                f"{value_column}:Q", title="Total (R$)", axis=alt.Axis(format="~s")
            ),
            tooltip=[
                alt.Tooltip("ano:O", title="Ano"),
                alt.Tooltip(f"{value_column}:Q", title="Total", format=".2f"),
            ],
        )
        .properties(title=title, width=800, height=300)
        .configure_axis(labelFontSize=12, titleFontSize=14)
        .configure_title(fontSize=16)
    )

    return chart


def create_monthly_summary_chart(monthly_data, value_column, title="Resumo Mensal"):
    """
    Cria um gráfico de barras para resumir valores por ano e mês.
    """
    chart = (
        alt.Chart(monthly_data)
        .mark_bar()
        .encode(
            x=alt.X("ano_mes:O", title="Ano-Mês", axis=alt.Axis(labelAngle=-45)),
            y=alt.Y(
                f"{value_column}:Q", title="Total (R$)", axis=alt.Axis(format="~s")
            ),
            tooltip=[
                alt.Tooltip("ano:O", title="Ano"),
                alt.Tooltip("mes:O", title="Mês"),
                alt.Tooltip(f"{value_column}:Q", title="Total", format=".2f"),
            ],
        )
        .properties(title=title, width=800, height=300)
        .configure_axis(labelFontSize=12, titleFontSize=14)
        .configure_title(fontSize=16)
    )

    return chart


import altair as alt


def create_monthly_line_chart(monthly_data, value_column, title="Resumo Mensal"):
    """
    Cria um gráfico de linha para resumir valores por ano e mês, cruzando por banco.

    Args:
        monthly_data (pd.DataFrame): DataFrame contendo os dados formatados (colunas 'ANO', 'MES', 'BANCO', 'ANO_MES' e valores).
        value_column (str): Nome da coluna que será usada para os valores (ex.: 'VALOR', 'CREDITO', 'DEBITO').
        title (str): Título do gráfico.

    Returns:
        alt.Chart: Gráfico Altair exibindo o resumo mensal cruzado por banco.
    """
    # Criar o gráfico de linha cruzando os dados por banco
    chart = (
        alt.Chart(monthly_data)
        .mark_line(point=True)
        .encode(
            x=alt.X("ano_mes:O", title="Ano-Mês", axis=alt.Axis(labelAngle=-45)),
            y=alt.Y(
                f"{value_column}:Q", title="Total (R$)", axis=alt.Axis(format="~s")
            ),
            color="banco:N",  # Cada banco com uma cor diferente
            tooltip=[
                alt.Tooltip("ano:O", title="Ano"),
                alt.Tooltip("mes:O", title="Mês"),
                alt.Tooltip("banco:N", title="Banco"),
                alt.Tooltip(f"{value_column}:Q", title="Total", format=".2f"),
            ],
        )
        .properties(title=title, width=800, height=300)
        .configure_axis(labelFontSize=12, titleFontSize=14)
        .configure_title(fontSize=16)
    )

    return chart


def create_yearly_line_chart(yearly_data, value_column, title="Resumo Anual"):
    """
    Cria um gráfico de linha para resumir valores por ano, cruzando por banco.
    """
    # Criar o gráfico de linha cruzando os dados por banco
    chart = (
        alt.Chart(yearly_data)
        .mark_line(point=True)
        .encode(
            x=alt.X("ano:O", title="Ano"),
            y=alt.Y(
                f"{value_column}:Q", title="Total (R$)", axis=alt.Axis(format="~s")
            ),
            color="banco:N",  # Cada banco com uma cor diferente
            tooltip=[
                alt.Tooltip("ano:O", title="Ano"),
                alt.Tooltip("banco:N", title="Banco"),
                alt.Tooltip(f"{value_column}:Q", title="Total", format=".2f"),
            ],
        )
        .properties(title=title, width=800, height=300)
        .configure_axis(labelFontSize=12, titleFontSize=14)
        .configure_title(fontSize=16)
    )

    return chart


def comparar_semanal(weekly_data):
    """
    - Cria um gráfico de barras para comparação de crédito, débito e saldo semanal.
    - weekly_data (pd.DataFrame): Dados semanais com crédito, débito e saldo.
    - Retorna o gráfico de barras semanal com cores personalizadas.
    """
    # Reestruturar os dados para o formato longo (long format)
    weekly_data = weekly_data.melt(
        id_vars="Semana",
        value_vars=["credito", "debito", "saldo"],
        var_name="Categoria",
        value_name="Valor",
    )

    # Definir cores personalizadas
    cores = {
        "saldo": "#007BFF",
        "debito": "#DC3545",
        "credito": "#28A745",
    }

    chart = (
        alt.Chart(weekly_data)
        .mark_bar()
        .encode(
            x=alt.X("Semana:N", title="Semana"),
            y=alt.Y("Valor:Q", title="Valor (R$)"),
            color=alt.Color(
                "Categoria:N",
                scale=alt.Scale(
                    domain=["saldo", "debito", "credito"], range=list(cores.values())
                ),
                legend=alt.Legend(title="Categoria"),
            ),
            tooltip=["Semana", "Categoria", "Valor"],
        )
        .properties(title="Ganhos e Gastos por Semana", width=600, height=400)
    )
    return chart


def comparar_mensal(monthly_data):
    """
    - Cria um gráfico de barras para comparação de crédito, débito e saldo mensal.
    - monthly_data (pd.DataFrame): Dados mensais com crédito, débito e saldo.
    - Retorna o gráfico de barras mensal com cores personalizadas.
    """
    # Reestruturar os dados para o formato longo (long format)
    monthly_data = monthly_data.melt(
        id_vars="Mês",
        value_vars=["credito", "debito", "saldo"],
        var_name="Categoria",
        value_name="Valor",
    )

    # Definir cores personalizadas
    cores = {
        "saldo": "#007BFF",
        "debito": "#DC3545",
        "credito": "#28A745",
    }

    chart = (
        alt.Chart(monthly_data)
        .mark_bar()
        .encode(
            x=alt.X("Mês:N", title="Mês"),
            y=alt.Y("Valor:Q", title="Valor (R$)"),
            color=alt.Color(
                "Categoria:N",
                scale=alt.Scale(
                    domain=["saldo", "debito", "credito"], range=list(cores.values())
                ),
                legend=alt.Legend(title="Categoria"),
            ),
            tooltip=["Mês", "Categoria", "Valor"],
        )
        .properties(title="Ganhos e Gastos por Mês", width=600, height=400)
    )
    return chart


def comparar_anual(yearly_data):
    """
    - Cria um gráfico de barras para comparação de crédito, débito e saldo anual.
    - yearly_data (pd.DataFrame): Dados anuais com crédito, débito e saldo.
    - Retorna o gráfico de barras anual com cores personalizadas.
    """
    # Reestruturar os dados para o formato longo (long format)
    yearly_data = yearly_data.melt(
        id_vars="Ano",
        value_vars=["credito", "debito", "saldo"],
        var_name="Categoria",
        value_name="Valor",
    )

    # Definir cores personalizadas
    cores = {
        "saldo": "#007BFF",
        "debito": "#DC3545",
        "credito": "#28A745",
    }

    chart = (
        alt.Chart(yearly_data)
        .mark_bar()
        .encode(
            x=alt.X("Ano:N", title="Ano"),
            y=alt.Y("Valor:Q", title="Valor (R$)"),
            color=alt.Color(
                "Categoria:N",
                scale=alt.Scale(
                    domain=["saldo", "debito", "credito"], range=list(cores.values())
                ),
                legend=alt.Legend(title="Categoria"),
            ),
            tooltip=["Ano", "Categoria", "Valor"],
        )
        .properties(title="Ganhos e Gastos por Ano", width=600, height=400)
    )
    return chart


def create_supplier_profit_chart(profitability):
    """
    Cria um gráfico de barras para mostrar a rentabilidade por fornecedor.
    """
    chart = alt.Chart(profitability).mark_bar().encode(
        x=alt.X('subconta', sort='-y', title='Fornecedor'),
        y=alt.Y('Rentabilidade', title='Rentabilidade Líquida (R$)'),
        color=alt.Color('subconta', legend=None),
        tooltip=['subconta', 'Receita', 'Despesa', 'Rentabilidade']
    ).properties(
        width=800,
        height=400,
        title='Rentabilidade por Fornecedor'
    )
    return chart


