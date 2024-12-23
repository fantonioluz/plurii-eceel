import pandas as pd
import streamlit as st

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

def prepare_credit_debit_data(data):
    """
    Prepara os dados para o gráfico de entradas e saídas mensais.
    """
    data["data"] = pd.to_datetime(data["data"])
    data["year_month"] = data["data"].dt.to_period("M")
    grouped = data.groupby("year_month")[["credito", "debito"]].sum().reset_index()
    grouped["year_month"] = grouped["year_month"].astype(str)
    return grouped


def prepare_account_data(data):
    """
    Prepara os dados para o gráfico de entradas e saídas por conta.
    """
    grouped_conta = data.groupby("conta")[["credito", "debito"]].sum().reset_index()
    return grouped_conta


def prepare_profit_data(data):
    """
    Prepara os dados para o gráfico de lucro ao longo do tempo.
    """
    data["data"] = pd.to_datetime(data["data"])
    data["year_month"] = data["data"].dt.to_period("M")
    grouped = data.groupby("year_month")[["credito", "debito"]].sum().reset_index()
    grouped["year_month"] = grouped["year_month"].astype(str)
    grouped["lucro"] = grouped["credito"] - grouped["debito"]
    return grouped


def prepare_yearly_account_data(data):
    """
    Prepara os dados para o gráfico de total de débito e crédito por ano e conta.
    """
    # Garantir que a coluna 'data' esteja no formato datetime
    data["data"] = pd.to_datetime(data["data"], errors='coerce')
    
    # Garantir que as colunas 'credito' e 'debito' sejam numéricas
    data["credito"] = pd.to_numeric(data["credito"], errors="coerce").fillna(0)
    data["debito"] = pd.to_numeric(data["debito"], errors="coerce").fillna(0)
    
    # Extrair o ano para agrupamento
    data["year"] = data["data"].dt.year
    
    # Agrupar por ano e conta
    grouped = data.groupby(["year", "conta"])[["credito", "debito"]].sum().reset_index()
    return grouped


def prepare_yearly_subaccount_data(data, conta):
    """
    Prepara os dados para o gráfico de total de débito e crédito por ano e subconta para uma conta específica.
    """
    # Garantir que a coluna 'data' esteja no formato datetime
    data["data"] = pd.to_datetime(data["data"], errors="coerce")

    # Garantir que as colunas 'credito' e 'debito' sejam numéricas
    data["credito"] = pd.to_numeric(data["credito"], errors="coerce").fillna(0)
    data["debito"] = pd.to_numeric(data["debito"], errors="coerce").fillna(0)

    # Extrair o ano para agrupamento
    data["year"] = data["data"].dt.year
    
    # Filtrar os dados pela conta especificada
    filtered_data = data[data["subconta"].str.strip().str.lower() == conta.strip().lower()]
    # Verificar se o DataFrame filtrado está vazio
    if filtered_data.empty:
        return pd.DataFrame()  # Retornar um DataFrame vazio para evitar erros

    # Agrupar por ano e subconta, somando os valores de crédito e débito
    grouped = (
        filtered_data.groupby(["year", "subconta"])[["credito", "debito"]]
        .sum()
        .reset_index()
    )

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
    data["mes"] = data[date_column].dt.month
    data["ano"] = data[date_column].dt.year
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

    return data[
        [
            "data",
            "descricao",
            "documento",
            "debito",
            "credito",
            "valor",
            "saldo",
            "banco",
            "conta",
            "subconta",
        ]
    ]


def comparar_calcular_total(data):
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
    def calcular_total_por_periodo(df, periodo_col, label):
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
    totais_semana = calcular_total_por_periodo(data, "semana", "Semana")
    totais_mes = calcular_total_por_periodo(data, "mes", "Mês")
    totais_ano = calcular_total_por_periodo(data, "ano", "Ano")

    return totais_semana, totais_mes, totais_ano

def get_yearly_summary(data, value_column):
    """
    Calcula o resumo anual de um valor especificado.
    """

    if "ano" not in data.columns:
        data["ano"] = data["ano"].dt.year
    yearly_summary = data.groupby("ano")[value_column].sum().reset_index()

    return yearly_summary


def get_monthly_summary(data, value_column):
    """
    Calcula o resumo mensal de um valor especificado, agrupado por ano e mês.
    """
    data["data"] = pd.to_datetime(data["data"])

    data["ano"] = data["data"].dt.year
    data["mes"] = data["data"].dt.month

    monthly_summary = data.groupby(["ano", "mes"])[value_column].sum().reset_index()

    # Add uma coluna formatada Ano-Mês
    monthly_summary["ano_mes"] = (
        monthly_summary["ano"].astype(str)
        + "-"
        + monthly_summary["mes"].astype(str).str.zfill(2)
    )

    return monthly_summary


def prepare_monthly_data_for_line_chart(data, value_column):
    """
    Prepara os dados mensais para o gráfico de linha, cruzando por banco.
    Returns:
        pd.DataFrame: DataFrame preparado com colunas 'ANO', 'MES', 'BANCO', 'ANO_MES' e o valor consolidado.
    """
    # Certifique-se de que a coluna DATA está no formato datetime
    data["data"] = pd.to_datetime(data["data"])

    # Adicionar colunas de ano e mês
    data["ano"] = data["data"].dt.year
    data["mes"] = data["data"].dt.month

    # Consolidar os valores por ano, mês e banco
    monthly_summary = (
        data.groupby(["ano", "mes", "banco"])[value_column].sum().reset_index()
    )

    # Adicionar uma coluna formatada para exibição no gráfico (Ano-Mês)
    monthly_summary["ano_mes"] = (
        monthly_summary["ano"].astype(str)
        + "-"
        + monthly_summary["mes"].astype(str).str.zfill(2)
    )

    return monthly_summary


def prepare_yearly_data_for_line_chart(data, value_column):
    """
    Prepara os dados anuais para o gráfico de linha, cruzando por banco.

    Args:
        data (pd.DataFrame): DataFrame contendo os dados.
        value_column (str): Nome da coluna que será usada para os valores (ex.: 'credito', 'debito').

    Returns:
        pd.DataFrame: DataFrame preparado com colunas 'ANO', 'BANCO' e o valor consolidado.
    """
    # Certifique-se de que a coluna DATA está no formato datetime
    data["data"] = pd.to_datetime(data["data"])

    # Consolidar os valores por ano e banco
    yearly_summary = data.groupby(["ano", "banco"])[value_column].sum().reset_index()

    return yearly_summary



def analyze_supplier_profitability(data):
    """
    Análise de rentabilidade por fornecedor com base em receitas e despesas, 
    considerando as colunas 'credito' e 'debito'.
    """
    # Filtrar as linhas relevantes para receitas e despesas com serviços
    service_data = data[data['conta'].isin(['Receita com serviços', 'Despesa com serviços'])]
    
    # Filtrar pelas marcas relevantes na subconta
    relevant_brands = ['Panasonic', 'Elgin', 'Spring', 'Fresnomaq']
    filtered_data = service_data[service_data['subconta'].isin(relevant_brands)]
    
    # Substituir "Spring" por "Springer" apenas para exibição
    filtered_data['subconta'] = filtered_data['subconta'].replace({'Spring': 'Springer'})
    
    # Garantir que as colunas 'credito' e 'debito' sejam numéricas
    filtered_data['credito'] = pd.to_numeric(filtered_data['credito'], errors='coerce').fillna(0)
    filtered_data['debito'] = pd.to_numeric(filtered_data['debito'], errors='coerce').fillna(0)
    
    # Criar a coluna 'Impacto' com tipo numérico
    filtered_data['Impacto'] = 0.0  # Inicializar como float

    # Adicionar receitas e subtrair despesas
    filtered_data.loc[filtered_data['conta'] == 'Receita com serviços', 'Impacto'] += filtered_data['credito']
    filtered_data.loc[filtered_data['conta'] == 'Despesa com serviços', 'Impacto'] -= filtered_data['debito']
    
    # Agrupar por subconta (marca) e calcular receita, despesa e rentabilidade
    profitability = filtered_data.groupby('subconta').agg(
        Receita=('credito', 'sum'),
        Despesa=('debito', 'sum'),
        Rentabilidade=('Impacto', 'sum')
    ).reset_index()
    
    # Calcular a rentabilidade como percentual que a marca representa do total das marcas
    profitability['Percentual'] = (profitability['Rentabilidade'] / profitability['Rentabilidade'].sum()) * 100
    #formartar com o valor em porcentagem com duas casas decimais
    profitability['Percentual'] = profitability['Percentual'].map("{:.2f}%".format)
    
    
    
    # Ordenar pela rentabilidade
    profitability = profitability.sort_values(by='Rentabilidade', ascending=False)
    
    
    return profitability





