import streamlit as st




# Cabeçalho principal
st.title("ECEEL - TEC")
st.markdown("### Olá, Mª Helena!")
st.write("Seja bem-vinda à sua área exclusiva de organização financeira, explore e impulsione seu negócio.")

# Imagem da usuária
col1, col2 = st.columns([1, 3])
with col1:
    st.image("src/images/Mask group.png", width=150, caption="Gestora")  # Ajuste o caminho, se necessário
with col2:
    st.write("### Mª Helena de Souza")
    st.write("**Status:** Nenhuma notificação no momento")

# Notificações
st.info("🔔 Não há nenhuma notificação no momento.")

# Botões de navegação
st.write("### Ações rápidas")
col1, col2 = st.columns(2)
with col1:
    if st.button("Ir ao Dashboard"):
        st.session_state.selected_page = "Dashboard Geral"
        st.query_params.update(page="Dashboard Geral")  # Redirecionar
with col2:
    if st.button("Histórico de Transações"):
        st.session_state.selected_page = "Histórico de Transações"
        st.query_params.update(page="Histórico de Transações")  # Redirecionar