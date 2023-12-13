import streamlit as st
from streamlit_option_menu import option_menu
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import folium
import random
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
            justify-content: center;
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


st.markdown("""
        <div style='text-align: center;'>
            <p>Esta é uma versão <strong>Beta</strong> da aplicação</a>.</p>
        </div>
    """, unsafe_allow_html=True)
# desenvolvida pelo <a href='https://ici.ong/'>Instituto do Câncer Infantil
# Rodapé
