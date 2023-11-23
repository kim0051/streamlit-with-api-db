import datetime
import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
from st_pages import Page, Section, hide_pages, add_page_title, show_pages

def checkPassword():
    """Returns `True` if the user had the correct password."""
    def validateData(username, password):
        if username == "admin" and password == "admin":
            st.session_state["password_correct"] = True
            return True
        else:
            st.error("The username or password you have entered is invalid.")
            st.session_state["password_correct"] = False
            return False
    if st.session_state.get("password_correct", False):
        return True
    username = st.text_input("Username")
    password = st.text_input("Password", type="password", key="password")
    st.button("Login", on_click=validateData, args=(username, password))
    return False

if not checkPassword():
    st.stop()

st.write(st.session_state['password_correct'])

if 'password_correct' in st.session_state:
    if st.session_state['password_correct']:
        add_page_title(layout="wide")
        show_pages(
            [
                Page("ewacs.py", "Dashboard", "⚒"),
                Section(name="Loader", icon=":apple:"),
                Page("menu/loader_performances.py", "Loader Performances", "🦿"),
                Page("menu/loader_status.py", "Loader Status", "🦵"),
                Section(name="Hauler", icon=":banana:"),
                Page("menu/hauler_performances.py", "Hauler Performances", "🦾"),
                Page("menu/hauler_status.py", "Hauler Status", "💪"),
                Page("menu/logs.py", "Log Data", "🧲", in_section=False),
                Page("menu/locations.py", "Location", "📌", in_section=False)
            ]
        )
    else:
        hide_pages(["Loader", "Hauler", "Log Data", "Location"])
        checkPassword()
else:
    hide_pages(["Loader", "Hauler", "Log Data", "Location"])
    checkPassword()