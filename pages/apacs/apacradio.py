import streamlit as st
import time
import pandas as pd


def apacradio():

    st.header('', divider='orange')
    st.title('APAC RADIO')
    st.write('Em construção')
    st.image("images/aviso.png", width=120)
    st.sidebar.title("Filtros Apac Radio")
    caminho_do_csv = 'apacRadio.csv'
    dadosradio = pd.read_csv(caminho_do_csv, encoding='utf-8')
    st.dataframe(dadosradio, use_container_width=True)
    st.metric('Quantidade de Apacs de Radioterapia em 10 anos', len(dadosradio))
