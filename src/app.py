import streamlit as st


home = st.Page("pages/home_page.py", title="Inicio", icon="🏠")
dashboard = st.Page("pages/dashboard_page.py", title="Dashboard", icon="📊")
bank = st.Page("pages/bank_page.py", title="Analise por Bancos", icon="🏦")
historic = st.Page("pages/historic_page.py", title="Historico de Transacoes", icon="📅")

st.markdown(
    """
    <style>
    .stMainBlockContainer.block-container {
        max-width: 100%; /* Altere para o tamanho desejado */
        padding: 2rem; /* Ajuste o espaçamento interno */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Configuração do menu manual
pg = st.navigation([home, dashboard, bank, historic])
pg.run()