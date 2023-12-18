import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
from streamlit_modal import Modal

st.set_page_config(
    page_title="Dashboard Oncologico",
    page_icon="bar_chart",
    layout="wide",
    initial_sidebar_state="expanded",
)

hide_st_style = """
    <style>
    MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)

with st.spinner():
    time.sleep(0.2)

st.markdown(
    """
    <style>
        .reportview-container {
            display: flex;
            flex-direction: column;
            min-height: 100vh;
            margin-top: 20px; /* Ajuste a margem superior conforme necessário */
            margin-bottom: 20px; /* Ajuste a margem inferior conforme necessário */
        }
        .main {
            width: 100%;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.header('Bem-vindo aos Dashboards de Oncológia Pediátrica', divider='orange')

st.write('Nestes dashboards, você terá acesso a informações abrangentes sobre oncologia pediátrica como:')
st.write("- Quantidade total de diagnósticos registrados.")
st.write("- Número de pacientes que iniciaram tratamento.")
st.write("- Dados sobre o tempo médio entre o diagnóstico e o início do tratamento.")
st.write("- Destaque para os diagnósticos mais frequentes em pacientes pediátricos.")
st.write("- Tipos mais comuns de tratamento inicial administrados.")
st.write("- locais de saúde habilitados em oncologia pediátrica.")
st.write("- Dados sobre mortalidade relacionados à oncologia pediátrica.")


def rodape():
    st.write('---')
    col1, col2 = st.columns(2)
    with col1:
        url_link = "https://ici.ong/"

        # URL da imagem
        url_imagem = "images/1.png"

        # Criar o link HTML
        link_html = f'<a href="{url_link}" target="_blank">https://ici.ong/</a>'

        # Exibir o link HTML usando st.markdown
        st.markdown(link_html, unsafe_allow_html=True)
        st.image('images/1.png', width=250)
    st.markdown(
        """
            | Versão **Beta** | © 2023
                """,
        unsafe_allow_html=True,)


rodape()
