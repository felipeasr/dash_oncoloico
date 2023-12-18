import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
    'RS': 'dados_Mortalidade2.csv',
    'RO': 'caminho_do_csv_RO.csv',
    'RR': 'caminho_do_csv_RR.csv',
    'SC': 'caminho_do_csv_SC.csv',
    'SP': 'caminho_do_csv_SP.csv',
    'SE': 'caminho_do_csv_SE.csv',
    'TO': 'caminho_do_csv_TO.csv'
}

# Verificar se a UF é válida e carregar os dados correspondentes
caminho_do_csv = caminhos_csv.get(selected_uf)


# visualização
if caminho_do_csv:
    df = pd.read_csv(caminho_do_csv, encoding='utf-8')
    ### Filtros ###
    casos_com = df[df['CAUSABAS'].str.startswith('C')]
    # Contar a quantidade de casos
    quantidade_obitos = len(casos_com)
    # Converter a coluna de datas para o tipo datetime

    def extrair_ano(data):
        return int(str(data)[-4:])

    df['Ano'] = df['DTOBITO'].apply(extrair_ano)

    # Agrupar por ano e contar o número de óbitos
    dados_agrupados = df.groupby('Ano').size().reset_index(name='Quantidade')
    # Criar um DataFrame com os dados
    top_causas = df['CAUSABAS'].value_counts().nlargest(10)
    df_top_causas = pd.DataFrame(
        {'Causa': top_causas.index, 'Quantidade': top_causas.values})

    top_localoco = df['LOCOCOR'].value_counts()
    df_top_localoco = pd.DataFrame(
        {'local': top_localoco.index, 'Quantidade': top_localoco.values})

    #### Criação de Graficos ####

    # Criar gráfico de barras interativo usando Plotly Express
    fig_Casos_anos = px.bar(dados_agrupados, x='Ano',
                            y='Quantidade', title='Óbitos por Ano')

    # Adicionar asterisco com a indicação '*preliminar' sobre a barra correspondente ao ano de 2022

    fig_Casos_anos.add_annotation(
        x=2022,
        text='preliminar',
        showarrow=True,
        arrowhead=2,
        # arrowcolor='rgba(50, 171, 96, 0.6)'
    )

    # Configurar o layout do gráfico
    fig_Casos_anos.update_layout(
        showlegend=True,
        font=dict(size=14),
        xaxis=dict(tickmode='array', tickvals=df['Ano']),
    )

    # Criar um gráfico de donuts usando Plotly
    fig_causabase = px.pie(df_top_causas, names='Causa', values='Quantidade', hole=0.4, title='Top 10 Causas Básicas de Óbito',
                           labels={'Causa': 'Causa Básica', 'Quantidade': 'Quantidade'})

    # Adicionar legenda
    fig_causabase.update_layout(legend=dict(title=dict(text='Legenda')))

    # Fig localocorrencia
    fig_localoco = px.pie(df_top_localoco, names='local', values='Quantidade', hole=0.4, title='locais de ocorrencia do Óbito',
                          labels={'local': 'local de Ocorrência', 'Quantidade': 'Quantidade'})

    #### View users ####
    st.info("Os dados são referentes ao período de 2013 a 2022. Os dados do ano de 2022 são preliminares e podem estar sujeitos a alterações.")

    prefixo = "Estado: "
    sufixo = ""
    # Defina o tamanho da fonte e a cor de fundo para a variável
    tamanho_da_fonte = "24px"
    cor_de_fundo = "#f3b54b"
    # Cor de fundo laranja
    # Use HTML embutido para destacar a variável com tamanho de fonte e cor de fundo
    st.markdown(
        f"<span style='font-size: {tamanho_da_fonte};'>"
        f"{prefixo}<span style='background-color: {cor_de_fundo};'>{selected_uf}</span>{sufixo}"
        "</span>",
        unsafe_allow_html=True
    )
    # st.write(f'Estado selecionado: {selected_uf}')
    st.markdown(
        f'<div>'
        f'<h4>Quantidade de obitos:</h4>'
        f'<p style="font-size: 25px;font-weight: bold">{quantidade_obitos}</p>'
        f'</div>',
        unsafe_allow_html=True
    )
    st.plotly_chart(fig_Casos_anos, use_container_width=True)
    st.plotly_chart(fig_causabase, use_container_width=True)
    st.plotly_chart(fig_localoco, use_container_width=True)

    st.write(df)
else:
    st.warning(
        'Selecione um estado na barra Lateral para carregar os dados.')
