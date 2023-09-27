
import streamlit as st
import folium
from streamlit_folium import st_folium
def map():
    with st.spinner():
        time.sleep(0.2)
    st.header('',divider='orange')
    # center on Liberty Bell, add marker
    m = folium.Map(location=[-28.91830464110885, -53.03546053071262], zoom_start=7)

    # call to render Folium map in Streamlit
    st_data = st_folium(m, width=1280,height=720)