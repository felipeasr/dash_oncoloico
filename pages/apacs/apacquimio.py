import streamlit as st
import time

def apacquimio():
    
    with st.spinner():
        time.sleep(0.2)
    st.header('',divider='orange')
    st.title('APAC QUIMIO')
    st.write('Em construção')
    st.image("images/aviso.png",width=120)
    st.sidebar.title("Filtros Apac Quimio")
    st.sidebar.selectbox('Selecione um Estabelecimento de Saúde:', [
        "Todos"])