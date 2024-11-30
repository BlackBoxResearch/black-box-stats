from static.elements import gradient_text
import streamlit as st

def SystemsPage():
    with st.container(border=False):    
        gradient_text("Systems", "2em")

if __name__ == "__main__":
    SystemsPage()
