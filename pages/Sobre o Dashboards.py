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
    page_title="Sobre Dashboard Oncologico",
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


def formata_numero(valor, prefixo=''):
    for unidade in ['', 'mil']:
        if valor < 1000:
            return f'{prefixo} {valor:.2f} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor:.2f} milhões'

  # Centralize todos os elementos
st.header('Dados dos Dashboards de Oncológia Pediátrica',
          divider='orange')

# Informações sobre a aplicação (centralizado)
st.subheader("Origem dos dados")
st.write(" Para o Painel Oncológico, são utilizados dados do Painel Oncológico DATASUS e do Cadastro Nacional de Estabelecimentos de Saúde (CNES).")
st.write(" Painel de Mortalidade, os dados são obtidos do Sistema de Informação sobre Mortalidade (SIM) - DATASUS.")
st.write(" Todos os dados são baixados de forma automatizada de uma pasta FTP do Datasus")

st.subheader("Preparação dos dados")
st.write(" Os arquivos são no formato DBC que é um DBF comprimido")
st.write(" Para facilitar a utilização desses dados, o primeiro passo é realizar a padronização para o formato CSV.")
st.write(" Esse processo é conduzido utilizando a linguagem de programação Python.")
st.write(" Inicialmente, verifica-se as variáveis de interesse para determinar quais informações serão incorporadas nos dashboards.")
st.write(" É feita uma verificação das variáveis quanto à presença de dados faltantes, os tipos das variáveis, garantindo a integridade das análises.")

st.subheader("Visualização dos dados")
st.write(" Os arquivos são no formato DBC que é um DBF comprimido")
st.write(" Os dados são transformados em gráficos para proporcionar uma visualização mais eficaz e intuitiva aos usuários.")
st.write(" Os dashboards são elaborados com layouts e design pensados para facilitar a interpretação das informações.")
st.write(" Possibilidade de interação com os gráficos para explorar detalhes específicos e obter insights mais aprofundados.")


st.subheader("Escolha das Bases de Dados")

st.write(" A seleção dessas bases de dados foi estrategicamente feita devido à integração abrangente das informações no painel de oncologia.")
st.write(" Os dados do painel oncologico são únicos, integrando informações dos seguintes sistemas:")
st.write("  - Sistema de Informação Ambulatorial (SIA) por meio do Boletim de Produção Ambulatorial Individualizado (BPA-I) e Autorização de Procedimento de Alta Complexidade (Apac),")
st.write("  - Sistema de Informação Hospitalar (SIH),")
st.write("  - Siscan.")
st.write("  - A base nacional do cartão SUS - CADSUS Web (Cadweb) foi utilizada para consolidar todos os possíveis números de CNS de um mesmo paciente em um único CNS master, promovendo assim a integração das bases de dados.")

st.write(" Optamos por incluir o Cadastro Nacional de Estabelecimentos de Saúde (CNES) para verificar a habilitação de cada hospital que atendeu crianças e adolescentes, enquanto o Sistema de Informação sobre Mortalidade (SIM) foi escolhido para acessar informações cruciais sobre mortalidade.")
