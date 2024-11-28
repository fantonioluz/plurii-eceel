import sqlite3
import pandas as pd

def load_data_from_db(db_path="bank_data_csv.db"):
    """
    Carrega os dados do banco SQLite.
    """
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM bank_transactions"
    df = pd.read_sql(query, conn)
    conn.close()
    return df
