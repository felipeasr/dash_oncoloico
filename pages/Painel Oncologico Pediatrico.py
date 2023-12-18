import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import pages.apacs.apacquimio as apacquimio
import pages.apacs.apacradio as apacradio

theme_plotly = None  # None or streamlit

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
# st.markdown(hide_st_style, unsafe_allow_html=True)
with st.spinner(''):
    time.sleep(0.5)


def cook_breakfast():
    msg = st.toast('Gathering ingredients...')
    time.sleep(1)
    msg.toast('Cooking...')
    time.sleep(1)
    msg.toast('Ready!', icon="🥞")


# if st.sidebar.button('Atualizar'):
#    cook_breakfast()
# Carregue seus dados CSV aqui
caminho_do_csv = 'painelIngles.csv'

dados2 = pd.read_csv(caminho_do_csv, encoding='utf-8')

st.title('Painel Oncologico Pediatrico :bar_chart:')

st.info(''' Os dados estão atualizados até :orange[Julho de 2023]''')


# Função para filtrar dados com base no estado selecionado
def filtrar_por_estado_diag(data, estado):
    if estado == "BR":
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
    if estado == "BR":
        return data['CNES_DIAG'].unique().tolist()
    else:
        return data[data['UF_TRATAM'] == estado]['CNES_TRAT'].unique().tolist()

# Função para filtrar dados com base no estado selecionado


def filtrar_por_estado_trat(data2, estado):
    if estado == "BR":
        return data2
    else:
        return data2[data2['UF_TRATAM'] == estado]

# Função para filtrar dados com base no estabelecimento selecionado


def filtrar_por_estabelecimento_trat(data2, estabelecimento):
    if estabelecimento == "Todos":
        return data2
    else:
        return data2[data2['CNES_TRAT'] == estabelecimento]

# Função para obter uma lista de estabelecimentos com base no estado selecionado


def obter_estabelecimentos_por_estado_trat(data2, estado):
    if estado == "BR":
        estabelecimentos = data2['CNES_TRAT'].unique().tolist()
    else:
        estabelecimentos = data2[data2['UF_TRATAM']
                                 == estado]['CNES_TRAT'].unique().tolist()

    # Ordena a lista alfabeticamente
    estabelecimentos.sort()

    return estabelecimentos

# Função para criar e exibir gráficos com base nos dados filtrados


def filtrar_por_estabelecimento_trat(data2, estabelecimento):
    if estabelecimento == "Todos":
        return data2
    else:
        return data2[data2['CNES_TRAT'] == estabelecimento]


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
    trat_mais_frequentes = data2.groupby(
        ['DIAG_DETH', 'UF_TRATAM']).size().unstack().fillna(0)
    trat_mais_frequentes['Total'] = trat_mais_frequentes.sum(axis=1)
    trat_mais_frequentes = trat_mais_frequentes.sort_values(
        by='Total', ascending=False).head(10)

    all_labels = set(trat_mais_frequentes.index) | set(
        diagnósticos_mais_frequentes.index)

    colors = px.colors.qualitative.Alphabet

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

    labels_abreviados = [label[:3]
                         for label in diagnósticos_mais_frequentes.keys()]

    fig_diagnósticos = go.Figure(data=[go.Pie(
        labels=diagnósticos_mais_frequentes.index,
        values=diagnósticos_mais_frequentes.values,
        hole=0.3,
        marker=dict(colors=[label_to_color[label]
                            for label in diagnósticos_mais_frequentes.index]),
        textinfo='percent + value'
    )])

    fig_diagnósticos.update_layout(
        title='10 Doenças diagnosticadas',
        legend=dict(
            orientation='v',  # Posição horizontal da legenda
            yanchor="bottom",  # Ancoragem da legenda na parte inferior
            y=-1.02,  # Distância vertical da legenda em relação ao gráfico
            xanchor="center",  # Ancoragem horizontal no centro
            x=0.5  # Posição horizontal da legenda no centro
        ),
        width=1000,
        height=800,
        font=dict(size=20),
    )

    fig_Trat = go.Figure(data=[go.Pie(
        labels=trat_mais_frequentes.index,
        values=trat_mais_frequentes['Total'],
        hole=0.3,
        marker=dict(colors=[label_to_color[label]
                    for label in trat_mais_frequentes.index]),
        textinfo='percent + value'
    )])

    fig_Trat.update_layout(
        title='10 Doenças tratadas',
        legend=dict(
            orientation='v',  # Posição horizontal da legenda
            yanchor="bottom",  # Ancoragem da legenda na parte inferior
            y=-1.02,  # Distância vertical da legenda em relação ao gráfico
            xanchor="center",  # Ancoragem horizontal no centro
            x=0.5  # Posição horizontal da legenda no centro
        ),
        width=1000,
        height=800,
        font=dict(size=20),
    )

    quanti_paciente_Trat_ANO = data2.groupby(
        'ANO_TRATAM')['UF_TRATAM'].count().reset_index()
    quanti_paciente_Trat_ANO.rename(columns={
        'ANO_TRATAM': 'Ano Tratamento', 'UF_TRATAM': 'Quantidade de Pacientes'}, inplace=True)

    total_pacientes_atendidos = quanti_paciente_Trat_ANO['Quantidade de Pacientes'].sum(
    )
    variavelauxmodalidade = data['TRATAMENTO'].value_counts()
    if not variavelauxmodalidade.empty:
        # Aqui, variavelauxmodalidade não está vazia, então você pode usá-la.
        variavelauxmodalidade = data['TRATAMENTO'].value_counts()
    else:
        # Caso contrário, use data2 para calcular os valores.
        variavelauxmodalidade = data2['TRATAMENTO'].value_counts()

    # Crie um gráfico Plotly Pie separadamente
    fig_modalidade = go.Figure(data=[go.Pie(
        labels=variavelauxmodalidade.index,
        values=variavelauxmodalidade.values,
        hole=0.3,
        textinfo='percent+label+value'
    )])
    fig_modalidade.update_layout(
        title='Primeiro tratamento registrado',
        legend=dict(
            orientation='v',

        ),
        width=1000,
        height=900,
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

    bins_tempo_tratamento = [-900, -61, -31, -1, 0, 10, 20, 30,
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
    variaveltabelacontagemaux = data['DIAG_DETH']
    if not variaveltabelacontagemaux.empty:
        variaveltabelacontagemaux = pd.crosstab(
            data['DIAG_DETH'], data['Categorias Tempo Tratamento'], margins=True, margins_name="Total")
    else:
        data2['Categorias Tempo Tratamento'] = pd.cut(
            data2['TEMPO_TRAT'], bins=bins_tempo_tratamento, labels=categorias_tempo_tratamento)
        # Adicione uma coluna "Total" para representar o total de casos em cada linha
        data2['Total'] = 1
        variaveltabelacontagemaux = pd.crosstab(
            data2['DIAG_DETH'], data2['Categorias Tempo Tratamento'], margins=True, margins_name="Total")

    variaveltabelacontagemGraficoaux = data['DIAG_DETH']
    if not variaveltabelacontagemGraficoaux.empty:
        variaveltabelacontagemGraficoaux = pd.crosstab(
            data['DIAG_DETH'], data['Categorias Tempo Tratamento'], margins=True, margins_name="Total")
    else:
        variaveltabelacontagemGraficoaux = pd.crosstab(
            data2['DIAG_DETH'], data2['Categorias Tempo Tratamento'], margins=True, margins_name="Total")

  # Exclua a coluna "Total" da tabela de contagem
    variaveltabelacontagemGraficoaux = variaveltabelacontagemGraficoaux.iloc[:-1, :-1]

    # Reorganize a tabela para que possa ser usada com o Plotly Sunburst
    variaveltabelacontagemGraficoaux.reset_index(inplace=True)
    tabela_contagem_melted = variaveltabelacontagemGraficoaux.melt(
        id_vars=['DIAG_DETH'], value_vars=variaveltabelacontagemGraficoaux.columns[1:])

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
        x=quanti_paciente_Trat_ANO['Ano Tratamento'],
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
    variavelauxsexo = data['SEXO'].value_counts()
    if not variavelauxsexo.empty:
        variavelauxsexo = data['SEXO'].value_counts()
    else:
        variavelauxsexo = data2['SEXO'].value_counts()

    # Crie um dicionário que mapeia os rótulos para as cores desejadas
    cores = {'Masculino': '#ADD8E6', 'Feminino': '#FFC0CB'}

    # Crie uma lista de cores com base nos rótulos no DataFrame
    cores_grafico = [cores[label] for label in variavelauxsexo.index]

    fig_donut = go.Figure(data=[go.Pie(
        labels=variavelauxsexo.index,
        values=variavelauxsexo.values,
        hole=0.3,
        textinfo='percent+ label+ value',
        marker_colors=cores_grafico  # Use a lista de cores personalizadas
    )])

    fig_donut.update_layout(
        title='Distribuição de casos por Sexo',
        legend=dict(
            orientation='v',

        ),
        width=1000,
        height=800,
        font=dict(size=20),
    )

    # Agrupe os dados por TRATAMENTO e DIAG_DETH e conte o número de ocorrências

    tabela_contagem2_aux = data['DIAG_DETH']
    if not tabela_contagem2_aux.empty:
        tabela_contagem2_aux = pd.crosstab(
            data['DIAG_DETH'], data['TRATAMENTO'], margins=True, margins_name="Total")
    else:
        tabela_contagem2_aux = pd.crosstab(
            data2['DIAG_DETH'], data2['TRATAMENTO'], margins=True, margins_name="Total")

    tabela_contagem_grafico2_aux = data['DIAG_DETH']
    if not tabela_contagem_grafico2_aux.empty:
        tabela_contagem_grafico2_aux = pd.crosstab(
            data['DIAG_DETH'], data['TRATAMENTO'], margins=True, margins_name="Total")
    else:
        tabela_contagem_grafico2_aux = pd.crosstab(
            data2['DIAG_DETH'], data2['TRATAMENTO'], margins=True, margins_name="Total")

    # Crie a tabela de contagem usando crosstab

    # Exclua a coluna "Total" da tabela de contagem
    tabela_contagem_grafico2_aux = tabela_contagem_grafico2_aux.iloc[:-1, :-1]

    # Reorganize a tabela para que possa ser usada com o Plotly Sunburst
    tabela_contagem_grafico2_aux.reset_index(inplace=True)
    tabela_contagem_melted2 = tabela_contagem_grafico2_aux.melt(
        id_vars=['DIAG_DETH'], value_vars=tabela_contagem_grafico2_aux.columns[1:])

    # Crie um gráfico Sunburst
    fig_primeiro_TRAT = px.sunburst(
        tabela_contagem_melted2,
        path=['DIAG_DETH', 'TRATAMENTO'],
        values='value',
        width=1200,  # Largura da figura
        height=1000,  # Altura da figura
        color_discrete_sequence=px.colors.sequential.Viridis,

    )

    # Personalize o layout do gráfico, se necessário
    fig_primeiro_TRAT.update_layout(
        title='Gráfico de Casos por Diagnóstico e Primeiro tratamento registrado'
    )

  # Filtrar os dados para população masculina e feminina
    dados_masculinos_aux = data[data['SEXO'] == 'Masculino'].copy()
    if not dados_masculinos_aux.empty:
        dados_masculinos_aux = data[data['SEXO'] == 'Masculino'].copy()
    else:
        dados_masculinos_aux = data2[data2['SEXO'] == 'Masculino'].copy()

    dados_femininos_aux = data[data['SEXO'] == 'Feminino'].copy()
    if not dados_femininos_aux.empty:
        dados_femininos_aux = data[data['SEXO'] == 'Feminino'].copy()
    else:
        dados_femininos_aux = data2[data2['SEXO'] == 'Feminino'].copy()

    # Adicionar uma coluna 'Sexo' para representar o sexo de cada linha
    dados_masculinos_aux['Sexo'] = 'Masculino'
    dados_femininos_aux['Sexo'] = 'Feminino'

    # Combinar os dados das duas populações
    dados_combinados = pd.concat([dados_masculinos_aux, dados_femininos_aux])

    # Contar a quantidade de diagnósticos para cada sexo e diagnóstico
    contagem_diag_sexo = dados_combinados.groupby(
        ['Sexo', 'DIAG_DETH']).size().reset_index(name='Quantidade')

    # Criar o treemap que mostra a população masculina e feminina
    fig_populacao_sexo = px.treemap(
        contagem_diag_sexo,
        path=[px.Constant('População'), 'Sexo', 'DIAG_DETH'],
        values='Quantidade',
        title='População Masculina e Feminina por Diagnóstico',
        color="Sexo",
        color_discrete_map={
            "(?)": "white", "Masculino": "#ADD8E6", "Feminino": "#FFC0CB", },
        height=800,
    )

    # Crie um filtro para hospitais habilitados
    hospitais_habilitados = data2[(data2['SGRUPHAB'].str[:4].isin(
        ['1709', '1713', '1711'])) & (data2['UF_TRATAM'])]

    # Crie um filtro para hospitais não habilitados em um estado específico
    hospitais_nao_habilitados = data2[(data2['SGRUPHAB'] == 'Sem Habilitação em Oncologia Pediátrica') & (
        data2['UF_TRATAM'])]

    # Crie um gráfico de pizza para exibir as porcentagens
    coreshab = ['#1f77b4', '#ff7f0e']

    graficohabilitacao = px.pie(
        names=['Habilitados', 'Não Habilitados'],
        values=[len(hospitais_habilitados), len(hospitais_nao_habilitados)],
        title=f'Porcentagem de Pacientes Tratados em Serviços Habilitados e Não Habilitados',
        color_discrete_sequence=coreshab  # Define as cores manualmente
    )

    # Personalize o gráfico, se necessário
    graficohabilitacao.update_traces(textinfo='percent+label+value')

    # Para garantir que a cor azul mais forte esteja associada à label "Habilitados",
    # você pode inverter a ordem das cores se necessário
    graficohabilitacao.update_traces(marker=dict(colors=coreshab[::-1]))

    prefixo = "Estado: "
    sufixo = ""
    # Defina o tamanho da fonte e a cor de fundo para a variável
    tamanho_da_fonte = "24px"
    cor_de_fundo = "#f3b54b"
    prefixo2 = "Região: "
    sufixo2 = ""
    # Defina o tamanho da fonte e a cor de fundo para a variável
    tamanho_da_fonte2 = "24px"
    cor_de_fundo2 = "#f3b54b"
    # Cor de fundo laranja
    # Use HTML embutido para destacar a variável com tamanho de fonte e cor de fundo
    if selected_regiao == "Todas":
        st.markdown(
            f"<span style='font-size: {tamanho_da_fonte};'>"
            f"{prefixo}<span style='background-color: {cor_de_fundo};'>{selected_estado}</span>{sufixo}"
            "</span>",
            unsafe_allow_html=True
        )
    elif selected_regiao != "Todas" and selected_estado != "BR":
        st.markdown(
            f"<span style='font-size: {tamanho_da_fonte};'>"
            f"{prefixo}<span style='background-color: {cor_de_fundo};'>{selected_estado}</span>{sufixo}"
            "</span>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<span style='font-size: {tamanho_da_fonte2};'>"
            f"{prefixo2}<span style='background-color: {cor_de_fundo2};'>{selected_regiao}</span>{sufixo2}"
            "</span>",
            unsafe_allow_html=True
        )

    if selected_estabelecimento != "Todos":
        estabelecimento_selecionado = dados_filtrados_trat[
            dados_filtrados_trat['CNES_TRAT'] == selected_estabelecimento]
        if not estabelecimento_selecionado.empty:
            st.subheader("DADOS DO ESTABELECIMENTO")

            # quadro de informações formatado com HTML personalizado
            st.markdown(
                f"""
                <table style="border: 2px solid #f4834e;  border-radius: 5px; font-size: 20px;">
                <tr >
                    <td style="font-weight: bold; padding: 8px;">Estabelecimento de Saúde:</td>
                    <td style="padding: 8px;">{selected_estabelecimento}</td>
                </tr>
                <tr>
                    <td style="font-weight: bold; padding: 8px;">Habilitação:</td>
                    <td style="padding: 8px;"> {estabelecimento_selecionado.iloc[0]["SGRUPHAB"]}</td>
                    <td style="font-weight: bold; padding: 8px;">Gestão:</td>
                    <td style="padding: 8px;">{estabelecimento_selecionado.iloc[0]["TPGESTAO"]}</td>
                </tr>
                </table>
                """,
                unsafe_allow_html=True,
            )
    # Adiciona espaço entre os quadros
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<hr style="border: 0.5px solid #d0d0d3; ; height: 0.5px;" />',
                unsafe_allow_html=True)

    if selected_estado != "BR" and selected_estabelecimento == "Todos" or selected_regiao != "Todas":
        st.plotly_chart(graficohabilitacao)
    # st.write(selected_estabelecimento)
    quantidade_pacientes = len(data)
    coluna1, coluna2 = st.columns(2)

    # Adicione um estilo CSS para tornar a borda fixa
    st.markdown(
        f'<style>'
        f'.fixed-border {{ position: sticky; top: 0; z-index: 1; background: white; }}'
        f'</style>',
        unsafe_allow_html=True
    )
    # Formata os números para o formato de milhares (com vírgula separadora de milhares)
    quantidade_pacientes_formatado = "{:,}".format(quantidade_pacientes)
    total_pacientes_atendidos_formatado = "{:,}".format(
        total_pacientes_atendidos)

    with coluna1:
        # Adicione a classe CSS "fixed-border" para tornar a borda fixa na primeira coluna
        st.markdown(

            f'<div style="border: 2px solid #f4834e; padding: 10px; border-radius: 5px; font-size: 20px;">'
            f'<h4>Quantidade de Pacientes Diagnosticados:</h4>'

            f'<p style="font-size: 25px;font-weight: bold">{quantidade_pacientes_formatado}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    with coluna2:
        st.markdown(
            f'<div style="border: 2px solid #f4834e; padding: 10px; border-radius: 5px; font-size: 20px;">'
            f'<h4>Quantidade de Pacientes Tratados:</h4>'
            f'<p style="font-size: 25px;font-weight: bold">{total_pacientes_atendidos_formatado}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.plotly_chart(fig3, use_container_width=True,)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_diagnósticos, use_container_width=True)

    with col2:
        st.plotly_chart(fig_Trat, use_container_width=True)
  # with st.expander("Veja mais informções"):
        # st.write("🖱️Dica Passe um pouse no grafico para ter mais informações")

    # Criar uma barra de divisão com estilo personalizado
    st.markdown('<hr style="border: 0.5px solid #d0d0d3; ; height: 0.5px;" />',
                unsafe_allow_html=True)
    st.plotly_chart(fig_donut, use_container_width=True)
    st.plotly_chart(fig_populacao_sexo, use_container_width=True)

    st.markdown('<hr style="border: 0.5px solid #d0d0d3; ; height: 0.5px;" />',
                unsafe_allow_html=True)

    # st.plotly_chart(fig_diagnósticos, use_container_width=True)
    # st.plotly_chart(fig_Trat, use_container_width=True)
    # st.write(tabela_relacao)
    st.plotly_chart(fig4)

    st.write(
        "Tabela de Contagem de Casos por Diagnóstico e Tempo do diagnostico ao primeiro Tratamento")
    st.dataframe(variaveltabelacontagemaux)
    with st.expander("Veja a Explicação"):
        st.write("Para os casos com informação de tratamento, o campo é composto de dois subcampos. O primeiro, de 1 dígito indica se o tratamento ocorreu antes ou depois do laudo de diagnóstico:")
        st.write(
            " - ( + ) tratamento com data registrada posterior ao laudo diagnóstico")
        st.write(
            " - ( - ) tratamento com data registrada anterior ao laudo diagnóstico")
    st.markdown('<hr style="border: 0.5px solid #d0d0d3; ; height: 0.5px;" />',
                unsafe_allow_html=True)
    st.plotly_chart(fig_modalidade, use_container_width=True)
    st.plotly_chart(fig_primeiro_TRAT, use_container_width=True)
    st.write(
        "Tabela de Contagem de Casos por Diagnóstico e Pirmeiro tratamento registrado")
    st.dataframe(tabela_contagem2_aux)

# Função para filtrar dados com base no estado e diagnóstico selecionados


def filtrar_por_diag(data, diagnosticos):
    if diagnosticos == "Todos":
        # Retorna todos os dados se "Todos" for selecionado
        return data
    else:
        # Filtra por diagnóstico
        return data[data['DIAG_DETH'] == diagnosticos]


# Barra lateral para seleção de estado
st.sidebar.title("Filtros")

# Barra lateral para seleção de diagnóstico
diagnosticos_unicos = sorted(dados2['DIAG_DETH'].unique())
# Adicione a opção "Todos" à lista de diagnósticos
diagnosticos_unicos.insert(0, "Todos")
selected_diagnosticos = st.sidebar.selectbox(
    'Selecione o Diagnóstico:', diagnosticos_unicos)  # Defina "Todos" como padr

anos_unicos = sorted(dados2['ANO_DIAGN'].unique())
selected_anos = st.sidebar.multiselect(
    'Selecione os Anos:', anos_unicos, default=anos_unicos)

# Lista de regiões do Brasil
regioes = ["Todas", "Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]

# Barra lateral para seleção de região
selected_regiao = st.sidebar.selectbox(
    'Selecione uma Região do Brasil:', regioes, index=0)

# Função para filtrar dados com base na região selecionada


def filtrar_por_regiao(data, regiao):
    if regiao == "Todas":
        # Retorna todos os dados se a região for "BR" (Brasil)
        return data
    elif regiao == "Norte":
        # Filtrar dados para a região Norte
        return data[data['UF_DIAGN'].isin(["AC", "AM", "AP", "PA", "RO", "RR", "TO"])]
    elif regiao == "Nordeste":
        # Filtrar dados para a região Nordeste
        return data[data['UF_DIAGN'].isin(["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"])]
    elif regiao == "Centro-Oeste":
        # Filtrar dados para a região Centro-Oeste
        return data[data['UF_DIAGN'].isin(["DF", "GO", "MS", "MT"])]
    elif regiao == "Sudeste":
        # Filtrar dados para a região Sudeste
        return data[data['UF_DIAGN'].isin(["ES", "MG", "RJ", "SP"])]
    elif regiao == "Sul":
        # Filtrar dados para a região Sul
        return data[data['UF_DIAGN'].isin(["PR", "RS", "SC"])]


# Função para obter a lista de estados com base na região selecionada
def obter_estados_por_regiao(regiao):
    if regiao == "Todas":
        # Retorna todos os estados se a região for "BR" (Brasil)
        return estados_unicos[1:]  # Exclua "BR" da lista
    elif regiao == "Norte":
        return ["AC", "AM", "AP", "PA", "RO", "RR", "TO"]
    elif regiao == "Nordeste":
        return ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"]
    elif regiao == "Centro-Oeste":
        return ["DF", "GO", "MS", "MT"]
    elif regiao == "Sudeste":
        return ["ES", "MG", "RJ", "SP"]
    elif regiao == "Sul":
        return ["PR", "RS", "SC"]


# Lista de estados únicos
estados_unicos = dados2['UF_DIAGN'].unique().tolist()

# Atualize a lista de estados com base na região selecionada
if selected_regiao != "Todas":
    estados_unicos = obter_estados_por_regiao(selected_regiao)

# Ordene a lista de estados em ordem alfabética
estados_unicos.sort()

# Adicione "BR" no topo da lista
estados_unicos.insert(0, "BR")

# Selecione o estado
selected_estado = st.sidebar.selectbox('Selecione um Estado:', estados_unicos)

# Barra lateral para seleção de estabelecimento
if selected_estado != "BR":
    selected_estabelecimento = st.sidebar.selectbox('Selecione um Estabelecimento de Saúde:', [
        "Todos"] + obter_estabelecimentos_por_estado_trat(dados2, selected_estado))
else:
    selected_estabelecimento = "Todos"

# Crie um intervalo de idades de 0 a 19 anos
idades_disponiveis = list(range(20))

# Substitua a opção "0 anos" por "Menos de 1 ano" para exibição
idades_disponiveis_display = ['Menos de 1 ano'] + \
    [str(i) for i in idades_disponiveis[1:]]

# Use multisseleção para faixa etária
selected_idades = st.sidebar.multiselect(
    "Selecione a Idade:", idades_disponiveis_display, default=idades_disponiveis_display)
st.sidebar.markdown('<hr style="border: 0.5px solid #d0d0d3; ; height: 0.5px;" />',
                    unsafe_allow_html=True)
# st.sidebar.download_button(
# label="Baixar Dados Brutos",
# data=dados2.to_csv(index=False).encode('utf-8'),Boa tarde, Professora Alice,
# file_name='dados_brutos.csv',
# key='download_button'
# )


def filtrar_por_idade(data, idades_selecionadas):
    # Mapeie a opção "Menos de 1 ano" para o valor real 0
    idades_reais = [0 if idade == 'Menos de 1 ano' else int(
        idade.split()[0]) for idade in idades_selecionadas]
    return data[data['IDADE'].isin(idades_reais)]


def filtrar_por_anos(data, anos):
    return data[data['ANO_DIAGN'].isin(anos)]


# Filtrar os dados de acordo com as seleções feitas
dados_filtrados_diag = filtrar_por_anos(dados2, selected_anos)
dados_filtrados_diag = filtrar_por_regiao(
    dados_filtrados_diag, selected_regiao)
dados_filtrados_diag = filtrar_por_estado_diag(
    dados_filtrados_diag, selected_estado)
dados_filtrados_diag = filtrar_por_estabelecimento_diag(
    dados_filtrados_diag, selected_estabelecimento)
dados_filtrados_diag = filtrar_por_idade(dados_filtrados_diag, selected_idades)
dados_filtrados_diag = filtrar_por_diag(
    dados_filtrados_diag, selected_diagnosticos)

dados_filtrados_trat = filtrar_por_anos(dados2, selected_anos)
dados_filtrados_trat = filtrar_por_regiao(
    dados_filtrados_trat, selected_regiao)
dados_filtrados_trat = filtrar_por_estado_trat(
    dados_filtrados_trat, selected_estado)
dados_filtrados_trat = filtrar_por_estabelecimento_trat(
    dados_filtrados_trat, selected_estabelecimento)
dados_filtrados_trat = filtrar_por_idade(dados_filtrados_trat, selected_idades)
dados_filtrados_trat = filtrar_por_diag(
    dados_filtrados_trat, selected_diagnosticos)
# dados_filtrados_trat.to_csv('teste.csv')
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
