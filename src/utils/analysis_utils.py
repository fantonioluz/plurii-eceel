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


def analyze_bank_transactions(data, start_date, end_date):
    """
    Filtra e agrega transações por banco e tipo (entradas/saídas).
    """
    # Converter coluna 'data' para datetime
    data['data'] = pd.to_datetime(data['data'])
    
    # Filtrar pelo intervalo de datas
    filtered_data = data[(data['data'] >= start_date) & (data['data'] <= end_date)]
    
    # Agregar entradas e saídas por banco
    bank_analysis = filtered_data.melt(
        id_vars=['banco'], 
        value_vars=['credito', 'debito'], 
        var_name='Tipo', 
        value_name='Valor'
    ).groupby(['banco', 'Tipo'], as_index=False)['Valor'].sum()
    
    return bank_analysis

def analyze_for_bank(banco_data):
    banco_analysis = banco_data.melt(
        id_vars=['data'], 
        value_vars=['credito', 'debito'], 
        var_name='Tipo', 
        value_name='Valor'
    ).groupby(['data', 'Tipo'], as_index=False)['Valor'].sum()
    return banco_analysis
