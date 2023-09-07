import streamlit as st


def pageabout():
    # Título da página
       
  # Centralize todos os elementos
    st.header('Bem-vindo aos Dashboards de Oncológia Pediátrica',divider='orange')
    
    
    # Informações sobre a aplicação (centralizado)
    st.markdown("""
        <div style='text-align: start;'>
            <p>Os dados contidos nesses dashboards são provenientes do <a href='https://opendatasus.saude.gov.br/'>OPENDATSUS</a>.</p>
            <p>Os dados do dashboard do painel oncológico estão atualizados até junho de 2023. Neste dashboard, você encontrará informações sobre a quantidade de casos por ano, local de atendimento, os maiores diagnósticos e tempo de tratamento em cada hospital.</p>
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

