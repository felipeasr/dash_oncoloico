import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import Pages.about as pageabout
# Carregue seus dados CSV aqui
caminho_do_csv = 'Painel_BR.csv'
dados2 = pd.read_csv(caminho_do_csv,encoding='utf-8')


def pagepo():
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
                orientation='v',
                font=dict(size=14),
            ),
            width=800,
            height=600,
            font=dict(size=20),
        )
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
                orientation='v',
                font=dict(size=14),
            ),
            width=800,
            height=600,
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
                orientation='v',
                font=dict(size=14),
            ),
            width=800,
            height=600,
            font=dict(size=20),
        )
       
        bins_tempo_tratamento = [ -91, -61, -31, -1, 0, 10, 20, 30, 40, 50, 60, 90, 120, 300, 365, 730,9999, float('inf')]


    # Defina as categorias de tempo de tratamento
        categorias_tempo_tratamento = ['-90 dias a -61 dias', '-60 dias a -31 dias', '-30 dias a -1 dia', 'mesmo dia (tempo 0 dia)', 
                                    '1 a 10 dias', '11 a 20 dias', '21 a 30 dias', '31 a 40 dias', '41 a 50 dias', '51 a 60 dias', 
                                    '61 a 90 dias', '91 a 120 dias', '121 dias a 300 dias', '301 dias a 365 dias', '366 a 730 dias', 
                                    'mais de dois anos','Sem Informação']

        
        

        #data2['TEMPO_TRAT'] = data2['TEMPO_TRAT'].replace(['99.999', '9999','99999.0','0.0'], 'Sem Informação')
        data['Categorias Tempo Tratamento'] = pd.cut(data['TEMPO_TRAT'], bins=bins_tempo_tratamento, labels=categorias_tempo_tratamento)

        # Adicione uma coluna "Total" para representar o total de casos em cada linha
        data['Total'] = 1

        # Crie a tabela de contagem usando crosstab
        tabela_contagem = pd.crosstab(data['DIAG_DETH'], data['Categorias Tempo Tratamento'], margins=True, margins_name="Total")    
        # Crie o gráfico de barras
        
        coluna1, coluna2 = st.columns(2)

        with coluna1:
            st.metric(
                'Quantidade de Pacientes Diagnosticados em 10 Anos', len(data))
            st.plotly_chart(fig, use_container_width=True)

        with coluna2:
            st.metric('Quantidade de Pacientes Tratados em 10 Anos',
                      total_pacientes_atendidos)
            st.plotly_chart(fig2, use_container_width=True)
        st.plotly_chart(fig_diagnósticos, use_container_width=True)
        st.plotly_chart(fig_Trat, use_container_width=True)
        #st.write(tabela_relacao)
        st.plotly_chart(fig_modalidade, use_container_width=False)
        st.write("Tabela de Contagem de Casos por Diagnóstico e Tempo de Tratamento")
        st.dataframe(tabela_contagem,use_container_width=True)

    # Barra lateral para seleção de estado
    st.sidebar.title("Filtros")
    # trat = dados2['UF_DIAGN']
    selected_estado = st.sidebar.selectbox(
        'Selecione um Estado:', ["Todos"] + dados2['UF_DIAGN'].unique().tolist())

    # Obtenha a lista de estabelecimentos com base no estado selecionado
    estabelecimentos_disponiveis = obter_estabelecimentos_por_estado_diag(
        dados2, selected_estado)

    # Barra lateral para seleção de estabelecimento
    if selected_estado != "Todos":
        selected_estabelecimento = st.sidebar.selectbox('Selecione um Estabelecimento:', [
            "Todos"] + obter_estabelecimentos_por_estado_diag(dados2, selected_estado))
    else:
        selected_estabelecimento = "Todos"

    selected_idade = st.sidebar.slider("Selecione uma faixa etária:", min_value=0, max_value=19, value=(0, 19))

    # Modifique as funções de filtragem para considerar a idade selecionada
    def filtrar_por_idade(data, idade_range):
        return data[(data['IDADE'] >= idade_range[0]) & (data['IDADE'] <= idade_range[1])]

    dados_filtrados_diag = filtrar_por_estado_diag(dados2, selected_estado)
    dados_filtrados_diag = filtrar_por_estabelecimento_diag(dados_filtrados_diag, selected_estabelecimento)
    dados_filtrados_diag = filtrar_por_idade(dados_filtrados_diag, selected_idade)

    dados_filtrados_trat = filtrar_por_estado_trat(dados2, selected_estado)
    dados_filtrados_trat = filtrar_por_estabelecimento_trat(dados_filtrados_trat, selected_estabelecimento)
    dados_filtrados_trat = filtrar_por_idade(dados_filtrados_trat, selected_idade)

    
    # Exibir gráficos com base nos dados filtrados

    exibir_graficos(dados_filtrados_diag, dados_filtrados_trat)
