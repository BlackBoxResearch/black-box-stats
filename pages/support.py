from static.elements import gradient_text
import streamlit as st

def SupportPage():
    with st.container(border=False):
        gradient_text("Support", "3em")

if __name__ == "__main__":
    SupportPage()
