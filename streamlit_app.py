import streamlit as st
from streamlit_extras.stylable_container import stylable_container

st.logo(image="static/bbs_type_logo.png", size="large")

def tile(key):
    return stylable_container(
        key=key,
        css_styles="""
        {
            background-color: #171717;
            border-radius: 0.5rem;
            padding: calc(1em - 1px);
            color: #ffffff;
        }
        """
    )

def gradient_tile(key):
    return stylable_container(
        key="key",
        css_styles="""
        {
            background: linear-gradient(135deg, #CDFFD8, #94B9FF);
            border-radius: 0.5rem;
            padding: 1em;
            color: #171717;
            display: flex;
            align-items: flex-start;
            justify-content: flex-start;
        }
        """
    )

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
        
    title, periods = st.columns(2, vertical_alignment="bottom")

    # ------ OVERVIEW STATS ------ #

    title.subheader("Overview", anchor=False)
    title.caption(f"General performance overview for account 80012345.")

    with periods:
        option_map = {
            0: "1D",
            1: "1W",
            2: "1M",
            3: "3M",
            4: "YTD",
            5: "All"
        }
        period_selection = st.segmented_control(
            "Period",
            options=option_map.keys(),
            format_func=lambda option: option_map[option],
            selection_mode="single",
            default=5
        )

    chart, stats = st.columns([3, 1], vertical_alignment="bottom")

    with chart:
        with tile("gain_chart"):
            with st.container(border=False, height=335):
                st.markdown("**Gain/Time**")

    with stats:
        with gradient_tile("performance_overview_stat_1"):
            with st.container(border=False, height=30):
                st.markdown(
                    """
                    <div style="line-height: 1.4;">
                        <p style="margin: 0; font-size: 0.75em; color: #171717;">AnalytiQ Score</p>
                        <p style="margin: 0; font-size: 1em; font-weight: bold; color: #171717;">78</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with tile("performance_overview_stat_2"):
            with st.container(border=False, height=30):
                st.markdown(
                    """
                    <div style="line-height: 1.4;">
                        <p style="margin: 0; font-size: 0.75em; color: #FFFFFF;">Win Rate</p>
                        <p style="margin: 0; font-size: 1em; font-weight: bold; color: #FFFFFF;">67.21%</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with tile("performance_overview_stat_3"):
            with st.container(border=False, height=30):
                st.markdown(
                    """
                    <div style="line-height: 1.4;">
                        <p style="margin: 0; font-size: 0.75em; color: #FFFFFF;">Profit Factor</p>
                        <p style="margin: 0; font-size: 1em; font-weight: bold; color: #FFFFFF;">1.12</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with tile("performance_overview_stat_4"):
            with st.container(border=False, height=30):
                st.markdown(
                    """
                    <div style="line-height: 1.4;">
                        <p style="margin: 0; font-size: 0.75em; color: #FFFFFF;">Average Win/Loss</p>
                        <p style="margin: 0; font-size: 1em; font-weight: bold; color: #FFFFFF;">1.53</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with tile("performance_overview_stat_5"):
            with st.container(border=False, height=30):
                st.markdown(
                    """
                    <div style="line-height: 1.4;">
                        <p style="margin: 0; font-size: 0.75em; color: #FFFFFF;">Most Traded Symbol</p>
                        <p style="margin: 0; font-size: 1em; font-weight: bold; color: #FFFFFF;">XAUUSD</p>
                    </div>
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

        st.markdown('''
                    ---
                    Created with ❤️ by [Black Box Research](https://blackboxresearch.com/).
                    ''')


# Set up the navigation
pg = st.navigation(pages, position="sidebar")
pg.run()
