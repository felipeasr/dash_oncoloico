import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import pages.apacs.apacquimio as apacquimio
import pages.apacs.apacradio as apacradio
import pages.maps.Mapa_Oncologico as map
import matplotlib.pyplot as plt
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
with st.spinner(''):
    time.sleep(0.5)


def cook_breakfast():
    msg = st.toast('Gathering ingredients...')
    time.sleep(1)
    msg.toast('Cooking...')
    time.sleep(1)
    msg.toast('Ready!', icon="🥞")


if st.sidebar.button('Atualizar'):
    cook_breakfast()
# Carregue seus dados CSV aqui
caminho_do_csv = 'Painel_BR.csv'
dados2 = pd.read_csv(caminho_do_csv, encoding='utf-8')


st.title('Painel Oncologico :bar_chart:')

st.markdown(''' Os dados estão atualizados até :orange[Julho de 2023]''')
# Função para filtrar dados com base no estado selecionado


def filtrar_por_estado_diag(data, estado):
    if estado == "Todos":
        return data
    else:
        return data[data['UF_DIAGN'] == estado]

# Função para filtrar dados com base no estabelecimento selecionado


def filtrar_por_estabelecimento_diag(data, estabelecimento):
    if estabelecimento == "Todos":
        return data
    else:
        return data[data['CNES_DIAG'] == estabelecimento]

# Função para obter uma lista de estabelecimentos com base no estado selecionado


def obter_estabelecimentos_por_estado_diag(data, estado):
    if estado == "Todos":
        return data['CNES_DIAG'].unique().tolist()
    else:
        return data[data['UF_DIAGN'] == estado]['CNES_DIAG'].unique().tolist()

# Função para filtrar dados com base no estado selecionado


def filtrar_por_estado_trat(data2, estado):
    if estado == "Todos":
        return data2
    else:
        return data2[data2['UF_TRATAM'] == estado]

# Função para filtrar dados com base no estabelecimento selecionado


def filtrar_por_estabelecimento_trat(data2, estabelecimento):
    if estabelecimento == "Todos":
        return data2
    else:
        return data2[data2['CNES_DIAG'] == estabelecimento]

# Função para obter uma lista de estabelecimentos com base no estado selecionado


def obter_estabelecimentos_por_estado_trat(data2, estado):
    if estado == "Todos":
        return data2['CNES_DIAG'].unique().tolist()
    else:
        return data2[data2['UF_TRATAM'] == estado]['CNES_DIAG'].unique().tolist()

# Função para criar e exibir gráficos com base nos dados filtrados


def exibir_graficos(data, data2):
    quanti_paciente_Diag_ANO = data.groupby(
        'ANO_DIAGN')['UF_DIAGN'].count().reset_index()
    quanti_paciente_Diag_ANO.rename(columns={
        'ANO_DIAGN': 'Ano Diagnóstico', 'UF_DIAGN': 'Quantidade de Pacientes'}, inplace=True)

    diagnósticos_mais_frequentes = data['DIAG_DETH'].value_counts().head(
        10)

    fig = px.bar(
        quanti_paciente_Diag_ANO,
        x='Ano Diagnóstico',
        y='Quantidade de Pacientes',
        title=f'Quantidade de Pacientes Diagnosticados por Ano',
        color_discrete_sequence=['#D5E5ED']
    )

    fig.update_layout(
        xaxis_title='Ano Diagnóstico',
        yaxis_title='Quantidade de Pacientes',
        showlegend=False,
        font=dict(size=14),
        width=800,
        height=600
    )

    fig.update_traces(
        text=quanti_paciente_Diag_ANO['Quantidade de Pacientes'], textposition='auto')
    trat_mais_frequentes = data2['DIAG_DETH'].value_counts().head(10)

    all_labels = set(trat_mais_frequentes.index) | set(
        diagnósticos_mais_frequentes.index)

    colors = px.colors.qualitative.Pastel
    # um dicionário de mapeamento de rótulos para cores em cada gráfico
    label_to_color = {}

# Atribua cores correspondentes aos rótulos presentes em ambos os gráficos
    for label in all_labels:
        if label in diagnósticos_mais_frequentes.index and label in trat_mais_frequentes.index:
            idx = list(all_labels).index(label)
            label_to_color[label] = colors[idx % len(colors)]


# Crie um conjunto de cores diferente para rótulos ausentes em ambos os gráficos
    remaining_labels = all_labels - set(label_to_color.keys())
    remaining_colors = px.colors.qualitative.Set3

    for idx, label in enumerate(remaining_labels):
        label_to_color[label] = remaining_colors[idx %
                                                 len(remaining_colors)]

    fig_diagnósticos = go.Figure(data=[go.Pie(
        labels=diagnósticos_mais_frequentes.index,
        values=diagnósticos_mais_frequentes.values,
        hole=0.3,
        marker=dict(colors=[label_to_color[label]
                            for label in diagnósticos_mais_frequentes.index]),
        textinfo='percent'
    )])

    fig_diagnósticos.update_layout(
        title='10 Doenças diagnosticadas',
        legend=dict(
            orientation='h',  # Posição horizontal da legenda
            yanchor="bottom",  # Ancoragem da legenda na parte inferior
            y=-1.02,  # Distância vertical da legenda em relação ao gráfico
            xanchor="center",  # Ancoragem horizontal no centro
            x=0.5  # Posição horizontal da legenda no centro
        ),
        width=1000,
        height=800,
        font=dict(size=20),)
    fig_Trat = go.Figure(data=[go.Pie(
        labels=trat_mais_frequentes.index,
        values=trat_mais_frequentes.values,
        hole=0.3,
        marker=dict(colors=[label_to_color[label]
                            for label in trat_mais_frequentes.index]),
        textinfo='percent'
    )])

    fig_Trat.update_layout(
        title='10 Doenças tratadas',
        legend=dict(
            orientation='h',  # Posição horizontal da legenda
            yanchor="bottom",  # Ancoragem da legenda na parte inferior
            y=-1.02,  # Distância vertical da legenda em relação ao gráfico
            xanchor="center",  # Ancoragem horizontal no centro
            x=0.5  # Posição horizontal da legenda no centro
        ),
        width=1000,
        height=800,
        font=dict(size=20),)

    quanti_paciente_Trat_ANO = data2.groupby(
        'ANO_TRATAM')['UF_TRATAM'].count().reset_index()
    quanti_paciente_Trat_ANO.rename(columns={
        'ANO_TRATAM': 'Ano Tratamento', 'UF_TRATAM': 'Quantidade de Pacientes'}, inplace=True)

    total_pacientes_atendidos = quanti_paciente_Trat_ANO['Quantidade de Pacientes'].sum(
    )
    modalidade = data['TRATAMENTO'].value_counts()

    # Crie um gráfico Plotly Pie separadamente
    fig_modalidade = go.Figure(data=[go.Pie(
        labels=modalidade.index,
        values=modalidade.values,
        hole=0.3,
        textinfo='percent'
    )])
    fig_modalidade.update_layout(
        title='Primeiro tratamento registrado',
        legend=dict(
            orientation='h',
            yanchor="bottom",
            y=-0.5,
            xanchor="center",
            x=0.5
        ),
        width=1000,
        height=800,
        font=dict(size=20),
    )

    fig2 = px.bar(
        quanti_paciente_Trat_ANO,
        x='Ano Tratamento',
        y='Quantidade de Pacientes',
        title=f'Quantidade de Pacientes Tratados por Ano',
        color_discrete_sequence=['#F6BDC0']
    )

    fig2.update_layout(
        xaxis_title='Ano Tratamento',
        yaxis_title='Quantidade de Pacientes',
        showlegend=False,
        font=dict(size=14),
        width=800,
        height=600

    )

    fig2.update_traces(
        text=quanti_paciente_Trat_ANO['Quantidade de Pacientes'], textposition='auto')

    color_palette = px.colors.qualitative.Pastel

    bins_tempo_tratamento = [-91, -61, -31, -1, 0, 10, 20, 30,
                             40, 50, 60, 90, 120, 300, 365, 730, 9999, float('inf')]

    # Defina as categorias de tempo de tratamento
    categorias_tempo_tratamento = ['-90 dias a -61 dias', '-60 dias a -31 dias', '-30 dias a -1 dia', 'mesmo dia (tempo 0 dia)',
                                   '1 a 10 dias', '11 a 20 dias', '21 a 30 dias', '31 a 40 dias', '41 a 50 dias', '51 a 60 dias',
                                   '61 a 90 dias', '91 a 120 dias', '121 dias a 300 dias', '301 dias a 365 dias', '366 a 730 dias',
                                   'mais de dois anos', 'Sem Informação']

    # data2['TEMPO_TRAT'] = data2['TEMPO_TRAT'].replace(['99.999', '9999','99999.0','0.0'], 'Sem Informação')
    data['Categorias Tempo Tratamento'] = pd.cut(
        data['TEMPO_TRAT'], bins=bins_tempo_tratamento, labels=categorias_tempo_tratamento)

    # Adicione uma coluna "Total" para representar o total de casos em cada linha
    data['Total'] = 1

    # Crie a tabela de contagem usando crosstab
    tabela_contagem = pd.crosstab(
        data['DIAG_DETH'], data['Categorias Tempo Tratamento'], margins=True, margins_name="Total")
    tabela_contagem_grafico = pd.crosstab(
        data['DIAG_DETH'], data['Categorias Tempo Tratamento'], margins=True, margins_name="Total")

   # Exclua a coluna "Total" da tabela de contagem
    tabela_contagem_grafico = tabela_contagem_grafico.iloc[:-1, :-1]

    # Reorganize a tabela para que possa ser usada com o Plotly Sunburst
    tabela_contagem_grafico.reset_index(inplace=True)
    tabela_contagem_melted = tabela_contagem_grafico.melt(
        id_vars=['DIAG_DETH'], value_vars=tabela_contagem_grafico.columns[1:])

    # Crie um gráfico Sunburst

    fig4 = px.sunburst(
        tabela_contagem_melted,
        path=['DIAG_DETH', 'Categorias Tempo Tratamento'],
        values='value',
        width=1200,  # Largura da figura
        height=1000,  # Altura da figura
    )

    # Personalize o layout do gráfico, se necessário
    fig4.update_layout(
        title='Gráfico de Casos por Diagnóstico e Tempo de Tratamento'
    )

    # Crie o gráfico de barras
    fig3 = go.Figure()

# Adicione o primeiro gráfico (quantidade de pacientes diagnosticados por ano)
    fig3.add_trace(go.Bar(
        x=quanti_paciente_Diag_ANO['Ano Diagnóstico'],
        y=quanti_paciente_Diag_ANO['Quantidade de Pacientes'],
        name='Diagnóstico',
        marker_color='#D5E5ED',
        text=quanti_paciente_Diag_ANO['Quantidade de Pacientes'],
        textposition='auto'
    ))

    # Adicione o segundo gráfico (quantidade de pacientes tratados por ano)
    fig3.add_trace(go.Bar(
        x=quanti_paciente_Diag_ANO['Ano Diagnóstico'],
        y=quanti_paciente_Trat_ANO['Quantidade de Pacientes'],
        name='Tratamento',
        marker_color='#F6BDC0',
        text=quanti_paciente_Trat_ANO['Quantidade de Pacientes'],
        textposition='auto'
    ))

    # Atualize o layout da figura diretamente
    fig3.update_layout(
        xaxis_title='Ano',
        yaxis_title='Quantidade de Pacientes',
        title='Quantidade de Pacientes Diagnosticados e Tratados por Ano',
        showlegend=True,
        font=dict(size=14),
        width=1980,
        height=600
    )

    fig3.update_xaxes(
        tickmode='array',
        tickvals=quanti_paciente_Diag_ANO['Ano Diagnóstico'],
    )
    sexo_counts = data['SEXO'].value_counts()

    fig_donut = go.Figure(data=[go.Pie(
        labels=sexo_counts.index,
        values=sexo_counts.values,
        hole=0.3,
        textinfo='percent'
    )])

    fig_donut.update_layout(
        title='Distribuição por Sexo',
        legend=dict(
            orientation='h',
            yanchor="bottom",
            y=-0.5,
            xanchor="center",
            x=0.5
        ),
        width=1000,
        height=800,
        font=dict(size=20),
    )

    # Agrupe os dados por TRATAMENTO e DIAG_DETH e conte o número de ocorrências
    # Crie a tabela de contagem usando crosstab
    tabela_contagem2 = pd.crosstab(
        data['DIAG_DETH'], data['TRATAMENTO'], margins=True, margins_name="Total")
    tabela_contagem_grafico2 = pd.crosstab(
        data['DIAG_DETH'], data['TRATAMENTO'], margins=True, margins_name="Total")

    # Exclua a coluna "Total" da tabela de contagem
    tabela_contagem_grafico2 = tabela_contagem_grafico2.iloc[:-1, :-1]

    # Reorganize a tabela para que possa ser usada com o Plotly Sunburst
    tabela_contagem_grafico2.reset_index(inplace=True)
    tabela_contagem_melted2 = tabela_contagem_grafico2.melt(
        id_vars=['DIAG_DETH'], value_vars=tabela_contagem_grafico2.columns[1:])

    # Crie um gráfico Sunburst
    fig_primeiro_TRAT = px.sunburst(
        tabela_contagem_melted2,
        path=['DIAG_DETH', 'TRATAMENTO'],
        values='value',
        width=1200,  # Largura da figura
        height=1000,  # Altura da figura
        color_discrete_sequence=px.colors.sequential.Viridis
    )

    # Personalize o layout do gráfico, se necessário
    fig_primeiro_TRAT.update_layout(
        title='Gráfico de Casos por Diagnóstico e Primeiro tratamento registrado'
    )

    # Crie um gráfico de mosaico
    coluna1, coluna2 = st.columns(2)

    # st.write(selected_estabelecimento)

    with coluna1:
        st.metric(
            'Quantidade de Pacientes Diagnosticados em 10 Anos', len(data))

    with coluna2:
        st.metric('Quantidade de Pacientes Tratados em 10 Anos',
                  total_pacientes_atendidos)

    st.plotly_chart(fig3, use_container_width=True,)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_diagnósticos, use_container_width=True)
        st.plotly_chart(fig_modalidade, use_container_width=True)

    with col2:
        st.plotly_chart(fig_Trat, use_container_width=True)

        st.plotly_chart(fig_donut, use_container_width=True)

    # st.plotly_chart(fig_diagnósticos, use_container_width=True)
    # st.plotly_chart(fig_Trat, use_container_width=True)
    # st.write(tabela_relacao)
    st.plotly_chart(fig4)
    st.write("Tabela de Contagem de Casos por Diagnóstico e Tempo de Tratamento")
    st.dataframe(tabela_contagem)
    st.plotly_chart(fig_primeiro_TRAT, use_container_width=True)
    st.write(
        "Tabela de Contagem de Casos por Diagnóstico e Pirmeiro tratamento registrado")
    st.dataframe(tabela_contagem2)
    # st.pyplot(plt)


    # Barra lateral para seleção de estado
st.sidebar.title("Filtros")

selected_estado = st.sidebar.selectbox(
    'Selecione um Estado:', ["Todos"] + dados2['UF_DIAGN'].unique().tolist())

# Obtenha a lista de estabelecimentos com base no estado selecionado
estabelecimentos_disponiveis = obter_estabelecimentos_por_estado_diag(
    dados2, selected_estado)

# Barra lateral para seleção de estabelecimento
if selected_estado != "Todos":
    selected_estabelecimento = st.sidebar.selectbox('Selecione um Estabelecimento de Saúde:', [
        "Todos"] + obter_estabelecimentos_por_estado_diag(dados2, selected_estado))
else:
    selected_estabelecimento = "Todos"

selected_idade = st.sidebar.slider(
    "Selecione uma faixa etária:", min_value=0, max_value=19, value=(0, 19))

# Modifique as funções de filtragem para considerar a idade selecionada


def filtrar_por_idade(data, idade_range):
    return data[(data['IDADE'] >= idade_range[0]) & (data['IDADE'] <= idade_range[1])]


# Dianostico
dados_filtrados_diag = filtrar_por_estado_diag(dados2, selected_estado)
dados_filtrados_diag = filtrar_por_estabelecimento_diag(
    dados_filtrados_diag, selected_estabelecimento)
dados_filtrados_diag = filtrar_por_idade(dados_filtrados_diag, selected_idade)
# Trat
dados_filtrados_trat = filtrar_por_estado_trat(dados2, selected_estado)
dados_filtrados_trat = filtrar_por_estabelecimento_trat(
    dados_filtrados_trat, selected_estabelecimento)
dados_filtrados_trat = filtrar_por_idade(dados_filtrados_trat, selected_idade)
# Exibir gráficos com base nos dados filtrados
exibir_graficos(dados_filtrados_diag, dados_filtrados_trat)
if selected_estado == "RS":

    Page_cliente = st.sidebar.selectbox(
        'APACS', ['Selecione uma Apac', 'Quimioterapia', 'Radioterapia'])

    if Page_cliente == 'Quimioterapia':
        apacquimio.apacquimio()

    if Page_cliente == 'Radioterapia':
        st.experimental_set_query_params()
        apacradio.apacradio()
   # map.map()
