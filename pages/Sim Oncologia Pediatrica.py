import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dashboard Oncologico",
    page_icon="bar_chart",
    layout="wide",
    initial_sidebar_state="auto",
)
hide_st_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.title('Mortalidade oncologica Pediatrica :bar_chart:')

# Lista de UF dos estados brasileiros
ufs = [
    '', 'RS',
    # 'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', #'MS', 'MG','PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO',
]

# Criando um seletor de UF na barra lateral
selected_uf = st.sidebar.selectbox('Selecione um estado:', ufs)

# Mapeamento dos caminhos dos arquivos CSV para cada UF
caminhos_csv = {
    'AC': 'caminho_do_csv_AC.csv',
    'AL': 'caminho_do_csv_AL.csv',
    'AP': 'caminho_do_csv_AP.csv',
    'AM': 'caminho_do_csv_AM.csv',
    'BA': 'caminho_do_csv_BA.csv',
    'CE': 'caminho_do_csv_CE.csv',
    'DF': 'caminho_do_csv_DF.csv',
    'ES': 'caminho_do_csv_ES.csv',
    'GO': 'caminho_do_csv_GO.csv',
    'MA': 'caminho_do_csv_MA.csv',
    'MT': 'caminho_do_csv_MT.csv',
    'MS': 'caminho_do_csv_MS.csv',
    'MG': 'caminho_do_csv_MG.csv',
    'PA': 'caminho_do_csv_PA.csv',
    'PB': 'caminho_do_csv_PB.csv',
    'PR': 'caminho_do_csv_PR.csv',
    'PE': 'caminho_do_csv_PE.csv',
    'PI': 'caminho_do_csv_PI.csv',
    'RJ': 'caminho_do_csv_RJ.csv',
    'RN': 'caminho_do_csv_RN.csv',
    'RS': 'Sim/mortalidadeInfantojuvenil.csv',
    'RO': 'caminho_do_csv_RO.csv',
    'RR': 'caminho_do_csv_RR.csv',
    'SC': 'caminho_do_csv_SC.csv',
    'SP': 'caminho_do_csv_SP.csv',
    'SE': 'caminho_do_csv_SE.csv',
    'TO': 'caminho_do_csv_TO.csv'
}

# Verificar se a UF é válida e carregar os dados correspondentes
caminho_do_csv = caminhos_csv.get(selected_uf)

if caminho_do_csv:
    dados = pd.read_csv(caminho_do_csv, encoding='utf-8')
    st.write(f'Estado selecionado: {selected_uf}')
    st.write(dados)
else:
    st.write('<u>Selecione um estado na barra Lateral para carregar os dados.</u>',
             unsafe_allow_html=True)
