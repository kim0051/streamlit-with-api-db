import datetime
import os
import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
from st_pages import Page, Section, hide_pages, add_page_title, show_pages

# This should be on top of your script
cookies = EncryptedCookieManager(
    # This prefix will get added to all your cookie names.
    # This way you can run your app on Streamlit Cloud without cookie name clashes with other apps.
    prefix="mycookies/streamlit-cookies-manager/",
    # You should really setup a long COOKIES_PASSWORD secret if you're running on Streamlit Cloud.
    password=os.environ.get("MY_COOKIES_PASSWORD", "D97D1EB28ACB9991CADDC7F58A84C"),
)

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
    st.write("Current cookies:", cookies)
    value = st.text_input("New value for a cookie")
    if st.button("Change the cookie"):
        cookies['a-cookie'] = value  # This will get saved on next rerun
        if st.button("No really, change it now"):
            cookies.save()  # Force saving the cookies now, without a rerun
            st.write("Cookies saved! "+str(cookies))

    username = st.text_input("Username")
    password = st.text_input("Password", type="password", key="password")
    st.button("Login", on_click=validateData, args=(username, password))
    return False

if not cookies.ready():
    # Wait for the component to load and send us current cookies.
    st.stop()

if not checkPassword():
    hide_pages(["Dashboard", "Loader", "Hauler", "Log Data", "Location"])
    st.markdown("""<style>[data-testid="stSidebar"] {display: none} [data-testid="collapsedControl"] { display: none }</style>""", unsafe_allow_html=True)
    st.stop()

st.write(st.session_state['password_correct'])

if 'password_correct' in st.session_state:
    if st.session_state['password_correct']:
        add_page_title(layout="wide")
        show_pages(
            [
                Page("main.py", "Dashboard", "⚒"),
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
        checkPassword()
else:
    checkPassword()