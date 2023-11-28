import streamlit as st
from st_pages import Page, Section, hide_pages, add_page_title, show_pages
import extra_streamlit_components as stx

# st.title("Login Page :door:")
# add_page_title(layout="wide")

@st.cache_resource(hash_funcs={"_thread.RLock": lambda _: None}, experimental_allow_widgets=True)
def get_manager():
    return stx.CookieManager()

st.set_page_config(page_title="Login Page", layout="wide", page_icon=":door:", menu_items=None)

st.title("Login Page :door:")

cookie_manager = get_manager()
cookie_manager.get_all()

def checkPassword():
    def validateData(username, password):
        if username == "" or password == "":
            st.error("Please fill username and password first.")
            return False
        if username == "admin" and password == "admin":
            cookie_manager.set("username", username)
            return True
        else:
            st.error("The username or password you have entered is invalid.")
            return False
    if cookie_manager.get(cookie="username") != None:
        return True
    username = st.text_input("Username")
    password = st.text_input("Password", type="password", key="password")
    st.button("Login", on_click=validateData, args=(username, password))
    return False

if not checkPassword():
    # show_pages([Page("main.py", "Login Page", ":door:")])
    # hide_pages(["Dashboard", "Loader", "Hauler", "Log Data", "Location"])
    # st.markdown("""<style>[data-testid="stSidebar"] {display: none} [data-testid="collapsedControl"] { display: none }</style>""", unsafe_allow_html=True)
    st.stop()

if cookie_manager.get(cookie="username") != None:
    show_pages(
        [
            Page("menu/dashboard.py", "Dashboard", "💼"),
            Section(name="Loader", icon=":apple:"),
            Page("menu/loader_performances.py", "Loader Performances", "🦿"),
            Page("menu/loader_status.py", "Loader Status", "🦵"),
            Section(name="Hauler", icon=":banana:"),
            Page("menu/hauler_performances.py", "Hauler Performances", "🦾"),
            Page("menu/hauler_status.py", "Hauler Status", "💪"),
            Page("menu/logs.py", "Log Data", "🧲", in_section=False),
            Page("menu/locations.py", "Location", "📌", in_section=False),
            Page("menu/logout.py", "Logout", ":no_entry_sign:", in_section=False)
        ]
    )
    hide_pages(["Login Page"])
    st.rerun()
else:
    checkPassword()