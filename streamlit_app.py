import streamlit as st
from streamlit_extras.stylable_container import stylable_container

st.logo(image="static/bbs_type_logo.png", size="large")

st.set_page_config(layout="centered")

def dashboard_page():
    with st.container(border=False):
        st.markdown(
                    """
                    <h3 style="
                        font-size: 2em;
                        background: linear-gradient(90deg, #CDFFD8, #94B9FF);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        font-weight: bold;
                        text-align: left;">
                        Welcome, Ben!
                    </h3>
                    """,
                    unsafe_allow_html=True
                )

def systems_page():
    with st.container(border=False):
        st.markdown(
                    """
                    <h3 style="
                        font-size: 2em;
                        background: linear-gradient(90deg, #CDFFD8, #94B9FF);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        font-weight: bold;
                        text-align: left;">
                        Systems
                    </h3>
                    """,
                    unsafe_allow_html=True
                )

def settings_page():
    with st.container(border=False):
        st.markdown(
                    """
                    <h3 style="
                        font-size: 2em;
                        background: linear-gradient(90deg, #CDFFD8, #94B9FF);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        font-weight: bold;
                        text-align: left;">
                        Settings
                    </h3>
                    """,
                    unsafe_allow_html=True
                )

def logout_page():
    st.header("Logout", anchor=False)

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

with st.sidebar:
    with st.container(border=True, height=240):
        st.markdown(
            """
            <h3 style="
                font-size: 1.5em;
                font-weight: bold;
                text-align: left;">
                Upgrade to pro for Life
            </h3>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            """
            <h3 style="
                font-size: 1em;
                background: linear-gradient(90deg, #CDFFD8, #94B9FF);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-weight: bold;
                text-align: left;">
                Limited lifetime deal ends soon
            </h3>
            """,
            unsafe_allow_html=True
        )
        st.caption("After this exclusive early access deal, we are switching to monthly/annual pricing.")
        # Button with a link using st.markdown
        st.markdown(
            """
            <div style="text-align: center;">
                <a href="https://pay.analytiq.trade/b/test_6oE0043QndEzbLi5kk" 
                    target="_blank" 
                    style="
                        display: inline-block; 
                        padding: 0.5em 1em; 
                        background-image: linear-gradient(90deg, #CDFFD8, #94B9FF); 
                        color: #111111; 
                        text-decoration: none; 
                        font-size: 0.85em;
                        border-radius: 0.5rem;
                        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
                    ">
                    ✨ Upgrade Now
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )


# Set up the navigation
pg = st.navigation(pages, position="sidebar")
pg.run()
