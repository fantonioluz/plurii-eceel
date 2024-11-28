import pandas as pd
import plotly.express as px

def clean_balance_column(data):
    """
    Limpa e converte a coluna 'saldo' para valores numéricos.
    """
    data['saldo'] = data['saldo'].str.replace('.', '', regex=False)  # Remove separadores de milhar
    data['saldo'] = data['saldo'].str.replace(',', '.', regex=False)  # Substitui vírgula decimal por ponto
    data['saldo'] = pd.to_numeric(data['saldo'], errors='coerce')  # Converte para float
    return data

def calculate_salary_expenses(data):
    """
    Calcula os gastos mensais com funcionários.
    """
    data['data'] = pd.to_datetime(data['data'])
    data['month'] = data['data'].dt.to_period('M').astype(str)
    salary_data = data[data['subconta'] == 'Salário']
    monthly_expenses = (
        salary_data.groupby('month')['debito']
        .sum()
        .reset_index()
        .rename(columns={'month': 'Mês', 'debito': 'Gastos com Funcionários'})
    )
    return monthly_expenses

def calculate_monthly_profit(data):
    """
    Calcula o lucro mensal (diferença entre créditos e débitos).
    """
    data['data'] = pd.to_datetime(data['data'])
    data['month'] = data['data'].dt.to_period('M').astype(str)
    profit_data = (
        data.groupby('month').apply(lambda x: x['credito'].sum() - x['debito'].sum())
        .reset_index(name='Lucro')
        .rename(columns={'month': 'Mês'})
    )
    return profit_data

# new functions
def prepare_credit_debit_data(data):
    """
    Prepara os dados para o gráfico de entradas e saídas mensais.
    """
    data['data'] = pd.to_datetime(data['data'])
    data['year_month'] = data['data'].dt.to_period('M')
    grouped = data.groupby('year_month')[['credito', 'debito']].sum().reset_index()
    grouped['year_month'] = grouped['year_month'].astype(str)
    return grouped

def prepare_account_data(data):
    """
    Prepara os dados para o gráfico de entradas e saídas por conta.
    """
    grouped_conta = data.groupby('conta')[['credito', 'debito']].sum().reset_index()
    return grouped_conta

def prepare_profit_data(data):
    """
    Prepara os dados para o gráfico de lucro ao longo do tempo.
    """
    data['data'] = pd.to_datetime(data['data'])
    data['year_month'] = data['data'].dt.to_period('M')
    grouped = data.groupby('year_month')[['credito', 'debito']].sum().reset_index()
    grouped['year_month'] = grouped['year_month'].astype(str)
    grouped['lucro'] = grouped['credito'] - grouped['debito']
    return grouped

def prepare_yearly_account_data(data):
    """
    Prepara os dados para o gráfico de total de débito e crédito por ano e conta.
    """
    data['data'] = pd.to_datetime(data['data'])
    data['year'] = data['data'].dt.year
    grouped = data.groupby(['year', 'conta'])[['credito', 'debito']].sum().reset_index()
    return grouped

def prepare_yearly_subaccount_data(data, conta):
    """
    Prepara os dados para o gráfico de total de débito e crédito por ano e subconta para uma conta específica.
    """
    data['data'] = pd.to_datetime(data['data'])
    data['year'] = data['data'].dt.year
    filtered_data = data[data['conta'] == conta]
    grouped = filtered_data.groupby(['year', 'subconta'])[['credito', 'debito']].sum().reset_index()
    return grouped

def convert_date_column(data, column_name):
    """
    Converte uma coluna para o tipo datetime.
    Returns:
        pd.DataFrame: DataFrame com a coluna convertida.
    """
    data[column_name] = pd.to_datetime(data[column_name])
    return data

def add_month_and_year_columns(data, date_column):
    """
    Adiciona colunas de mês e ano ao DataFrame com base em uma coluna de data.
    Returns:
        pd.DataFrame: DataFrame com colunas de mês e ano.
    """
    data['month'] = data[date_column].dt.month
    data['year'] = data[date_column].dt.year
    return data

def transform_data_for_display_in_table(data):
    """
    Transforma o DataFrame para exibição:
    - Remove a hora da coluna de data, exibindo apenas YYYY-MM-DD.
    - Consolida as colunas 'credito' e 'debito' em uma única coluna 'valor'.
      Débitos são representados como valores negativos.
    """
    data["data"] = pd.to_datetime(data["data"])

    data["data"] = data["data"].dt.date

    data["valor"] = data["credito"] - data["debito"]

    data = data.sort_values(by="data")

    return data[["data", "descricao", "documento", "debito", "credito","valor", "saldo", "banco", "conta", "subconta"]]


def calculate_total(data):
    """
    - Calcula os totais de crédito, débito e saldo para os últimos 3 períodos: semanas, meses e anos.
    """
    # Converter a coluna de data para datetime
    data["data"] = pd.to_datetime(data["data"])

    # Adicionar colunas para semana, mês e ano
    data["semana"] = data["data"].dt.to_period("W").apply(lambda r: r.start_time)
    data["mes"] = data["data"].dt.to_period("M").apply(lambda r: r.start_time)
    data["ano"] = data["data"].dt.year

    # Função para calcular totais por período
    def calculate_total_per_period(df, periodo_col, label):
        df_periodo = (
            df.groupby(periodo_col)
            .agg({"credito": "sum", "debito": "sum"})
            .reset_index()
        )
        df_periodo["saldo"] = df_periodo["credito"] - df_periodo["debito"]
        df_periodo = df_periodo.sort_values(periodo_col, ascending=False).head(3)
        df_periodo = df_periodo.rename(columns={periodo_col: label})
        return df_periodo

    # Calcular totais para semanas, meses e anos
    totais_semana = calculate_total_per_period(data, "semana", "Semana")
    totais_mes = calculate_total_per_period(data, "mes", "Mês")
    totais_ano = calculate_total_per_period(data, "ano", "Ano")

    return totais_semana, totais_mes, totais_ano


def create_weekly_chart(weekly_data):
    """
    - Cria um gráfico de barras para comparação de crédito, débito e saldo semanal.
    - weekly_data (pd.DataFrame): Dados semanais com crédito, débito e saldo.
    - Gráfico de barras semanal.
    """
    fig = px.bar(
        weekly_data,
        x="Semana",
        y=["credito", "debito", "saldo"],
        title="Ganhos e Gastos por Semana",
    )
    return fig


def create_monthly_chart(monthly_data):
    """
    - Cria um gráfico de barras para comparação de crédito, débito e saldo mensal.
    - monthly_data (pd.DataFrame): Dados mensais com crédito, débito e saldo.
    - Gráfico de barras mensal.
    """
    fig = px.bar(
        monthly_data,
        x="Mês",
        y=["credito", "debito", "saldo"],
        title="Ganhos e Gastos por Mês",
    )
    return fig


def create_yearly_chart(yearly_data):
    """
    - Cria um gráfico de barras para comparação de crédito, débito e saldo anual.
    - yearly_data (pd.DataFrame): Dados anuais com crédito, débito e saldo.
    - Gráfico de barras anual.
    """
    fig = px.bar(
        yearly_data,
        x="Ano",
        y=["credito", "debito", "saldo"],
        title="Ganhos e Gastos por Ano",
    )
    return fig
