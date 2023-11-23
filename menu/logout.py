import streamlit as st
from st_pages import add_page_title

add_page_title(layout="wide")

st.error("Do you really, wanna logout from this apps?")
if st.button("Yes Go Ahead"):
    st.success("You have been logged out!")
    st.session_state["password_correct"] = False
    st.button(login.py)