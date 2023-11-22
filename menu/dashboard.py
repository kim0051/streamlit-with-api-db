import streamlit as st
from st_pages import add_page_title
import requests
import pandas as pd

add_page_title(layout="wide")

# st.write("This is just a sample page!")
response_API = requests.get('http://localhost:8080/ewacspro/api/load-data/PAMA2/LoaderPerformances')
data = response_API.json()
    
col1, col2 = st.columns(2)
with col1:
    button1 = st.button('First Page')
with col2:
    button2 = st.button('Last Page')

if(button1):
    response_API = requests.get(data["first_page_url"])
    data = response_API.json()
if(button2):
    response_API = requests.get(data["last_page_url"])
    data = response_API.json()


# totalcol = len(data["links"])
# st.write("Total data: ", totalcol)
df = pd.DataFrame(data["data"])

st.dataframe(df, use_container_width=True)
st.write("Current page: ", data["current_page"])

def pagination():
    # if(st.button('First Page')):
    #     response_API = requests.get(data["first_page_url"])
    #     data = response_API.json()
    # if(st.button('Last Page')):
    #     response_API = requests.get(data["last_page_url"])
    #     data = response_API.json()
    for x in data["links"]:
        if(bool(x["url"]) == True):
            if(st.button(x["label"])):
                response_API = requests.get(x["url"])
                data = response_API.json()