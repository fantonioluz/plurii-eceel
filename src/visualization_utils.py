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


def create_credit_debit_chart(grouped):
    """
    Cria um gráfico de barras para entradas e saídas (Crédito e Débito) mensais lado a lado.
    """
    chart = alt.Chart(grouped).transform_fold(
        ['credito', 'debito'],
        as_=['Tipo', 'Valor']
    ).mark_bar().encode(
        x=alt.X('year_month:O', title='Mês'),
        y=alt.Y('Valor:Q', title='Valor (R$)'),
        color='Tipo:N',
        xOffset='Tipo:N',
        tooltip=[alt.Tooltip('year_month:O', title='Mês'), alt.Tooltip('Valor:Q', title='Valor (R$)', format='.2f')]
    ).properties(
        width=800,
        height=400,
        title='Entradas e Saídas Mensais (Crédito e Débito)'
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        fontSize=16
    )

    return chart


def create_account_chart(grouped_conta):
    """
    Cria um gráfico de barras para entradas e saídas por conta.
    """
    return alt.Chart(grouped_conta).transform_fold(
        ['credito', 'debito'],
        as_=['Tipo', 'Valor']
    ).mark_bar().encode(
        x=alt.X('conta:O', title='Conta'),
        y=alt.Y('Valor:Q', title='Valor (R$)'),
        color='Tipo:N',
        tooltip=[alt.Tooltip('conta:O', title='Conta'), alt.Tooltip('Valor:Q', title='Valor (R$)', format='.2f')]
    ).properties(
        width=800,
        height=400,
        title='Entradas e Saídas por Conta (Crédito e Débito)'
    )

def create_yearly_account_chart(grouped):
    """
    Cria um gráfico de barras para total de débito e crédito por ano e conta.
    """
    chart = alt.Chart(grouped).transform_fold(
        ['credito', 'debito'],
        as_=['Tipo', 'Valor']
    ).mark_bar().encode(
        x=alt.X('year:O', title='Ano'),
        y=alt.Y('Valor:Q', title='Valor (R$)'),
        color='Tipo:N',
        column='conta:N',
        tooltip=[alt.Tooltip('year:O', title='Ano'), alt.Tooltip('Valor:Q', title='Valor (R$)', format='.2f')]
    ).properties(
        width=150,
        height=400,
        title='Total de Débito e Crédito por Ano e Conta'
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        fontSize=16
    )

    return chart

def create_yearly_subaccount_chart(grouped, conta):
    """
    Cria um gráfico de barras para total de débito e crédito por ano e subconta para uma conta específica.
    """
    # Ordenar subcontas por maior despesa (débito) dentro de cada ano 
    sorted_grouped = grouped.sort_values(by=['year', 'debito'], ascending=[True, False])

    chart = alt.Chart(sorted_grouped).transform_fold(
        ['credito', 'debito'],
        as_=['Tipo', 'Valor']
    ).mark_bar().encode(
        x=alt.X('year:O', title='Ano'),
        y=alt.Y('Valor:Q', title='Valor (R$)'),
        color='Tipo:N',
        column='subconta:N',
        tooltip=[alt.Tooltip('year:O', title='Ano'), alt.Tooltip('Valor:Q', title='Valor (R$)', format='.2f')]
    ).properties(
        width=150,
        height=400,
        title=f'Total de Débito e Crédito por Ano e Subconta ({conta})'
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        fontSize=16
    )

    return chart

def create_yearly_summary_chart(yearly_data, value_column, title="Resumo Anual"):
    """
    Cria um gráfico de barras ou linhas para resumir valores por ano.
    """
    chart = alt.Chart(yearly_data).mark_bar().encode(
        x=alt.X("ano:O", title="Ano"),
        y=alt.Y(f"{value_column}:Q", title="Total (R$)", axis=alt.Axis(format="~s")),
        tooltip=[
            alt.Tooltip("ano:O", title="Ano"),
            alt.Tooltip(f"{value_column}:Q", title="Total", format=".2f")
        ]
    ).properties(
        title=title,
        width=800,
        height=400
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        fontSize=16
    )

    return chart

