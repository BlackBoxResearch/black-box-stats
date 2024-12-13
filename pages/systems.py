import streamlit as st
from static.elements import tile

primary_background = '#111111'
secondary_background = '#171717'
dark_text_color = '#171717'
light_text_color = '#E8E8E8'
color_1 = '#5A85F3' #Blue
color_2 = '#CDFFD8' #Green
border_color = '#3c3c3c'
caption_color = '#878884'


def SystemsPage():
    with st.container(border=False):    
        st.subheader("Systems", anchor=False)

        with tile(
            key="systems_metric",
            height=50,
            border=True
        ):
            st.metric(
                label="Test Stat",
                value="50")
        
        

if __name__ == "__main__":
    SystemsPage()

        #                /* background-image: url('static/container_background.png'); /*