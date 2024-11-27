import sqlite3
import pandas as pd
import os

# Caminho do banco de dados SQLite
csv_database_path = "bank_data_csv.db"
csv_database_path = os.path.abspath(csv_database_path)  # Caminho absoluto

# Garantir que o diretório do banco de dados exista
os.makedirs(os.path.dirname(csv_database_path), exist_ok=True)

# Conectar ao banco de dados
conn = sqlite3.connect(csv_database_path)

# Criar a tabela se ainda não existir
schema = """
CREATE TABLE IF NOT EXISTS bank_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data DATE NOT NULL,
    descricao TEXT NOT NULL,
    documento TEXT,
    credito REAL DEFAULT 0,
    debito REAL DEFAULT 0,
    saldo REAL DEFAULT 0,
    banco TEXT NOT NULL,
    conta TEXT,
    subconta TEXT,
    file_path TEXT
);
"""
cursor = conn.cursor()
cursor.execute(schema)

# Caminho do CSV
csv_path = "./data/processed/df_concat.csv"  # Atualize o caminho, se necessário
csv_path = os.path.abspath(csv_path)

# Carregar os dados do CSV
df = pd.read_csv(csv_path)

# Verificar e ajustar o formato das colunas, se necessário
df['data'] = pd.to_datetime(df['DATA'], errors='coerce')  # Converte a data para o formato correto
df['saldo'] = pd.to_numeric(df['SALDO'], errors='coerce')  # Garante que o saldo seja numérico
df = df.rename(columns=str.lower)  # Normaliza os nomes das colunas

# Popular o banco de dados
df[['data', 'descricao', 'documento', 'credito', 'debito', 'saldo', 'banco','conta','subconta', 'file_path']].to_sql(
    'bank_transactions', conn, if_exists='append', index=False
)

conn.commit()
conn.close()

print(f"Banco de dados populado com sucesso a partir do CSV em: {csv_database_path}")
