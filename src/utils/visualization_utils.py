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