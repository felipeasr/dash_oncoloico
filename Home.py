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
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
hide_st_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
with st.spinner('Wait for it...'):
    time.sleep(0.5)


#Funçoes
def cook_breakfast():
    msg = st.toast('Gathering ingredients...')
    time.sleep(1)
    msg.toast('Cooking...')
    time.sleep(1)
    msg.toast('Ready!', icon = "🥞")

if st.sidebar.button('Atualizar'):
    cook_breakfast()

def formata_numero(valor, prefixo = ''):
    for unidade in ['', 'mil']:
        if valor <1000:
            return f'{prefixo} {valor:.2f} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor:.2f} milhões'



       
  # Centralize todos os elementos
st.header('Bem-vindo aos Dashboards de Oncológia Pediátrica',divider='orange')
    
    
    # Informações sobre a aplicação (centralizado)
st.markdown("""
        <div style='text-align: start;'>
            <p>Os dados contidos nesses dashboards são provenientes do <a href='https://opendatasus.saude.gov.br/'>OPENDATSUS</a>.</p>
            <p>Os dados do dashboard do painel oncológico estão atualizados até Julho de 2023. Neste dashboard, você encontrará informações sobre a quantidade de casos por ano, local de atendimento, os maiores diagnósticos e tempo de tratamento em cada hospital.</p>
        </div>
    """, unsafe_allow_html=True)

    # Centralize o texto
st.markdown("""
        <div style='text-align: center;'>
            <p>Esta é uma versão <strong>Beta</strong> da aplicação desenvolvida pelo <a href='https://ici.ong/'>Instituto do Câncer Infantil</a>.</p>
        </div>
    """, unsafe_allow_html=True)
col1, col2, col3 = st.columns([5,5,5])

with col1:
     st.write("")

with col2:
      st.image("images/1.png")
      
with col3:
     st.write("")


