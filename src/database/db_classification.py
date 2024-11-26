import sqlite3

# Caminho do banco de dados SQLite
csv_database_path = "bank_data_csv.db"

# Conectar ao banco de dados
conn = sqlite3.connect(csv_database_path)
cursor = conn.cursor()

# Adicionar a coluna "categoria" se não existir
cursor.execute("""
    ALTER TABLE bank_transactions
    ADD COLUMN categoria TEXT DEFAULT 'Outros'
""")
conn.commit()

# Atualizar as transações para classificar como "Salário dos Funcionários"
cursor.execute("""
    UPDATE bank_transactions
    SET categoria = 'Salário dos Funcionários'
    WHERE descricao LIKE '%PRO-LABORE%'
""")

conn.commit()
cursor.execute("""
    UPDATE bank_transactions
    SET categoria = 'Salário dos Funcionários'
    WHERE descricao LIKE '%SALARIO%'
""")

conn.commit()
conn.close()

print("Transações classificadas com sucesso.")
