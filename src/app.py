import streamlit as st


home = st.Page("pages/home_page.py", title="Inicio", icon="🏠")
dashboard = st.Page("pages/dashboard_page.py", title="Dashboard", icon="📊")
bank = st.Page("pages/bank_page.py", title="Analise por Bancos", icon="🏦")

# Configuração do menu manual
pg = st.navigation([home, dashboard, bank])
pg.run()