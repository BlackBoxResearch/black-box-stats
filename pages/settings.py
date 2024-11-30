from static.elements import gradient_text
import streamlit as st

def SettingsPage():
    with st.container(border=False):
        gradient_text("Settings", "2em")

if __name__ == "__main__":
    SettingsPage()
