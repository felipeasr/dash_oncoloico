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
from streamlit_elements import elements, mui, html

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
with st.spinner('...'):
    time.sleep(0.5)

def formata_numero(valor, prefixo=''):
    for unidade in ['', 'mil']:
        if valor < 1000:
            return f'{prefixo} {valor:.2f} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor:.2f} milhões'

  # Centralize todos os elementos
st.header('Bem-vindo aos Dashboards de Oncológia Pediátrica', divider='orange')

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
col1, col2, col3 = st.columns([5, 5, 5])

with col1:
    st.write("")

with col2:
    st.image("images/1.png")

with col3:
    st.write("")

with elements("nivo_charts"):

    # Streamlit Elements includes 45 dataviz components powered by Nivo.

    from streamlit_elements import nivo

    DATA = [
        { "taste": "fruity", "chardonay": 93, "carmenere": 61, "syrah": 114 },
        { "taste": "bitter", "chardonay": 91, "carmenere": 37, "syrah": 72 },
        { "taste": "heavy", "chardonay": 56, "carmenere": 95, "syrah": 99 },
        { "taste": "strong", "chardonay": 64, "carmenere": 90, "syrah": 30 },
        { "taste": "sunny", "chardonay": 119, "carmenere": 94, "syrah": 103 },
    ]

    with mui.Box(sx={"height": 500}):
        nivo.Radar(
            data=DATA,
            keys=[ "chardonay", "carmenere", "syrah" ],
            indexBy="taste",
            valueFormat=">-.2f",
            margin={ "top": 70, "right": 80, "bottom": 40, "left": 80 },
            borderColor={ "from": "color" },
            gridLabelOffset=36,
            dotSize=10,
            dotColor={ "theme": "background" },
            dotBorderWidth=2,
            motionConfig="wobbly",
            legends=[
                {
                    "anchor": "top-left",
                    "direction": "column",
                    "translateX": -50,
                    "translateY": -40,
                    "itemWidth": 80,
                    "itemHeight": 20,
                    "itemTextColor": "#999",
                    "symbolSize": 12,
                    "symbolShape": "circle",
                    "effects": [
                        {
                            "on": "hover",
                            "style": {
                                "itemTextColor": "#000"
                            }
                        }
                    ]
                }
            ],
            theme={
                "background": "#FFFFFF",
                "textColor": "#31333F",
                "tooltip": {
                    "container": {
                        "background": "#FFFFFF",
                        "color": "#31333F",
                    }
                }
            }
        )
with elements("style_mui_sx"):

    # For Material UI elements, use the 'sx' property.
    #
    # <Box
    #   sx={{
    #     bgcolor: 'background.paper',
    #     boxShadow: 1,
    #     borderRadius: 2,
    #     p: 2,
    #     minWidth: 300,
    #   }}
    # >
    #   Some text in a styled box
    # </Box>

    mui.Box(
        "Some text in a styled box",
        sx={
            "bgcolor": "background.paper",
            "boxShadow": 1,
            "borderRadius": 2,
            "p": 2,
            "minWidth": 300,
        }
    )