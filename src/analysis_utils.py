import pandas as pd

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
