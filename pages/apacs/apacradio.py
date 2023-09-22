import streamlit as st
import time

def apacradio():
    
    with st.spinner():
        time.sleep(0.2)
    st.header('',divider='orange')
    st.title('APAC RADIO')
    st.write('Em construção')
    st.image("images/aviso.png",width=120)
    st.sidebar.title("Filtros Apac Radio")