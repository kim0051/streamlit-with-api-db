import streamlit as st
from streamlit_folium import st_folium
import folium

from st_pages import add_page_title

add_page_title(layout="wide")

st.write("Location with folium")

data = folium.Map(location=[0.516755, 117.535089], zoom_start=15)
folium.Marker([0.516755, 117.535089], popup='<i>Sangatta Utara</i>').add_to(data)

st_folium(data, use_container_width=True, height=500)