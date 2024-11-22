import streamlit as st
from streamlit_extras.stylable_container import stylable_container

st.logo(image="static/bbs_type_logo.png", icon_image="static/bbs-icon.png", size="large")

st.set_page_config(layout="centered")

def dashboard_page():
    with st.container(border=True):
        st.title("Welcome, Ben!", anchor=False)

def systems_page():
    st.title("Systems", anchor=False)

def settings_page():
    st.title("Settings", anchor=False)

def logout_page():
    st.title("Logout", anchor=False)

# Define pages as a dictionary of page groups and individual pages
pages = {
    "Home": [
        st.Page(dashboard_page, title="Dashboard", icon=":material/dashboard:"),
        st.Page(systems_page, title="Systems", icon=":material/ssid_chart:"),
    ],
    "Settings": [
        st.Page(settings_page, title="Settings", icon=":material/settings:"),
        st.Page(logout_page, title="Logout", icon=":material/logout:"),
    ],
}

# Set up the navigation
pg = st.navigation(pages, position="sidebar")
pg.run()
