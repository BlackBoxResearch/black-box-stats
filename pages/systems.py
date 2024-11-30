from static.elements import gradient_text
import streamlit as st

def SystemsPage():
    with st.container(border=False):    
        col1, col2 = st.columns(2)
        with col1:
            gradient_text("Systems", "2em")

if __name__ == "__main__":
    SystemsPage()
