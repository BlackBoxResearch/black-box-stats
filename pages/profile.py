from static.elements import gradient_text
import streamlit as st

def ProfilePage():
    with st.container(border=False):
        gradient_text("My Profile", "2em")

if __name__ == "__main__":
    ProfilePage()
