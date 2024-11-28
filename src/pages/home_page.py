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

