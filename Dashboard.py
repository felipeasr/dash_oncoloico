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
import Pages.Dash.po as pagepo
import Pages.about as pageabout



st.set_page_config(
    page_title="Dashboard DataSUS",
    page_icon="bar_chart",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

with st.spinner('Wait for it...'):
    time.sleep(2)


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


Page_cliente = st.sidebar.selectbox(
    'Dashboards', ['Sobre','Painel Oncologico', 'Sim'], 0)
if Page_cliente == 'Sobre':
    #st.experimental_set_query_params()
    pageabout.pageabout()
if Page_cliente == 'Painel Oncologico':
    #st.experimental_set_query_params()
    pagepo.pagepo()
