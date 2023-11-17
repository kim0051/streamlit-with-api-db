import streamlit as st
from st_pages import add_page_title
import requests
import pandas as pd

add_page_title(layout="wide")

# st.write("This is just a sample page!")
response_API = requests.get('http://localhost:8080/ewacspro/api/load-data/PAMA2/LoaderPerformances')
data = response_API.json()
df = pd.DataFrame(data["data"])
st.dataframe(df, use_container_width=True)