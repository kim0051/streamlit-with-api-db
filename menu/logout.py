import streamlit as st
from st_pages import Page, add_page_title, show_pages
import extra_streamlit_components as stx

add_page_title(layout="wide")

@st.cache_resource(hash_funcs={"_thread.RLock": lambda _: None}, experimental_allow_widgets=True)
def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()
cookie_manager.get_all()
st.warning("Do you really, wanna logout from this apps?")
if st.button("Logout"):
    cookie_manager.delete("username")
    show_pages([Page("main.py", "Login Page", ":door:")])
    st.stop()