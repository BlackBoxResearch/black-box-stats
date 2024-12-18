import streamlit as st
from streamlit_extras.stylable_container import stylable_container

# Gradient colors
color_start = "#000000"  # Black
color_end = "#1a1a3b"  # Dark blue

def ProfilePage():
    with st.container(border=False):
        st.subheader("My Profile", anchor=False)

        col1, col2 = st.columns(2, vertical_alignment="top")
        with col1:
            with stylable_container(
                key="glass",
                css_styles=f'''
            {{
                padding: calc(1em - 1px);
                background: rgba(255, 255, 255, 0.04);
                border-radius: 0.5rem;
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
                backdrop-filter: blur(11.1px);
                -webkit-backdrop-filter: blur(11.1px);
            }}
            '''
            ):
                with st.container(border=False, height=50):
                    st.markdown(
                        f"""
                            <div style="line-height: 1.5;">
                                <p style="margin: 0; font-size: 0.8em; color: '#171717';">Stat 1</p>
                                <p style="margin: 0; font-size: 1.2em; font-weight: bold; color: '#171717';">Value 1</p>
                            </div>
                            """,
                        unsafe_allow_html=True
                    )
        
        with col2:
            with stylable_container(
                key="glass2",
                css_styles=f'''
            {{
                padding: calc(1em - 1px);
                background: rgba(255, 255, 255, 0.04);
                border-radius: 0.5rem;
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
                backdrop-filter: blur(11.1px);
                -webkit-backdrop-filter: blur(11.1px);
            }}
            '''
            ):
                with st.container(border=False, height=50):
                    st.markdown("TEST")
        



if __name__ == "__main__":
    ProfilePage()
