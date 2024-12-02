from static.elements import gradient_text
import streamlit as st

def ProfilePage():
    with st.container(border=False):
        st.subheader("My Profile", anchor=False)

if __name__ == "__main__":
    ProfilePage()
