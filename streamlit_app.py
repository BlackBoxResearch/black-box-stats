import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from sqlalchemy.sql import text  # Import text from sqlalchemy
import time

st.set_page_config(layout="centered")
st.logo(image="static/bbs_type_logo.png", size="large")

def metric_tile(key, stat, value, height, type):
    """
    Creates a stylable metric tile using a custom container in Streamlit.

    Args:
        key (str): Unique key for the tile.
        stat (str): The title or label of the metric.
        value (str): The value to display for the metric.
        height (int): Height of the container in pixels.
        type (str): primary (#171717 background), secondary (Gradient Background).
    """

    if type == "primary":
        text_color = "#ffffff"

        with tile(key, height):
            st.markdown(
                f"""
                    <div style="line-height: 1.4;">
                        <p style="margin: 0; font-size: 0.75em; color: {text_color};">{stat}</p>
                        <p style="margin: 0; font-size: 1em; font-weight: bold; color: {text_color};">{value}</p>
                    </div>
                    """,
                unsafe_allow_html=True
            )

        
    elif type == "secondary":
        text_color = "#171717"

        with gradient_tile(key, height):
            st.markdown(
                f"""
                    <div style="line-height: 1.4;">
                        <p style="margin: 0; font-size: 0.75em; color: {text_color};">{stat}</p>
                        <p style="margin: 0; font-size: 1em; font-weight: bold; color: {text_color};">{value}</p>
                    </div>
                    """,
                unsafe_allow_html=True
            )

def tile(key, height):
    with stylable_container(
        key=key,
        css_styles="""
        {
            background-color: #171717;
            border-radius: 0.5rem;
            padding: calc(1em - 1px);
            color: #ffffff;
        }
        """
    ):
        return st.container(border=False, height=height)
    
def gradient_tile(key, height):
    with stylable_container(
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
    ):
        return st.container(border=False, height=height)

def gradient_button(label, key, icon):
    """
    Creates a stylable button using a custom container in Streamlit.

    Args:
        label (str): Button text.
        key (str): Unique key for the tile.
        icon (str): Button material icon, e.g. ":material/check:".
    """
    with stylable_container(
            # border: 1px solid #434343;
            key="confirm_add_account_button",
            css_styles="""
                        button {
                            background: linear-gradient(135deg, #CDFFD8, #94B9FF);
                            border-radius: 0.5rem;
                            color: #171717;
                        }

                        button:active {
                            transform: scale(0.98);
                        }
                        """,
    ):
        return st.button(label=label, key=key, icon=icon, use_container_width=True)

def gradient_text(text, font_size):
    """
    Creates text with a gradient colour in Streamlit.

    Args:
        text (str): Text to display.
        font_size (str): Text size, eg. 1em or 10px.
    """
    
    return st.markdown(
                    f"""
                    <h3 style="
                        font-size: {font_size};
                        background: linear-gradient(90deg, #CDFFD8, #94B9FF);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        font-weight: bold;
                        text-align: left;">
                        {text}
                    </h3>
                    """,
                    unsafe_allow_html=True
                )

def execute_query(query, params=None):
    """
    Executes a read-only SQL query and returns the result.
    Args:
        query (str): The SQL query to execute.
        params (dict): Parameters for the query, if any.
    Returns:
        list: List of rows resulting from the query.
    """
    conn = st.connection('analytiq_db', type='sql')
    with conn.session as s:
        try:
            # Mark the query as a text object
            result = s.execute(text(query), params or {})
            return result.fetchall()
        except Exception as e:
            st.error(f"Error executing query: {e}")
            return []

def get_user_accounts(user_id):
    """
    Retrieves a list of account numbers for a given user ID where the connection status is 'connected'.
    Args:
        user_id (int): The ID of the user.
    Returns:
        list: A list of account numbers associated with the user.
    """
    # Query to get the account numbers for the user
    query = '''
        SELECT account_number
        FROM accounts
        WHERE user_id = :user_id
        AND connection_status IS 'connected'
    '''

    # Execute the query using the helper function
    result = execute_query(query, {'user_id': user_id})

    # Extract and return the account_number values
    account_numbers = [row[0] for row in result]
    return account_numbers

def dashboard_page():
    with st.container(border=False):
        gradient_text("Welcome, Ben!", "2em")

def accounts_page():
    with st.container(border=False):
        gradient_text("My Accounts", "2em")

        user_id = 1

        # Get the list of account numbers for the user
        account_numbers = get_user_accounts(user_id)

        # Prepare the account number options for the selectbox
        if account_numbers:
            account_options = account_numbers
        else:
            account_options = ["No accounts available"]
        col1, col2 = st.columns(2, vertical_alignment="bottom")

        # Create the selectbox with the retrieved account number options
        with col1:
            account_selection = st.selectbox("Select Account", account_options)

        with col2:
            @st.dialog("Add Account")
            def add_account_dialog():
                account_number = st.text_input("Account Number", placeholder="Account Number")
                password = st.text_input("Investor Password", placeholder="Investor Password", type="password")
                server = st.text_input("Server", placeholder="Server")
                platform = st.selectbox("Platform", ("mt4", "mt5"), placeholder="Platform")

                confirm_add_account_button = gradient_button("Add Account", key="confirm_add_account_button", icon=":material/check:")

                if confirm_add_account_button:
                    with st.spinner("Adding your account..."):
                        time.sleep(2)
                    st.success("Account successfully added! (TEST)")
                    time.sleep(2)
                    st.rerun()

            open_add_account_dialog = gradient_button(label="Add Account", key="open_add_account_dialog", icon=":material/add_circle:")

            if open_add_account_dialog: add_account_dialog()

        # Check if an account is selected (ensure account_selection is not "No accounts available")
        if account_selection and account_selection != "No accounts available":

            tab1, tab2, tab3, tab4, tab5 = st.tabs(["Performance", "Trade Journal", "Analytic Tools", "AI Insights", "Settings"])

            with tab1: # ------ PERFORMANCE STATS ------ #
                
                # ------ OVERVIEW ------ #

                st.subheader("Overview", anchor=False)
                st.caption(f"General performance overview for account {account_selection}.")

                chart, stats = st.columns([3, 1], vertical_alignment="bottom")

                with chart:
                    with tile("overview_chart", 385):
                        st.markdown("**Overview**")

                with stats:
                    metric_tile("performance_overview_stat_1", "Total Gain", "12.36%", 40, "secondary")
                    metric_tile("performance_overview_stat_2", "Win Rate", "67.21%", 40, "primary")
                    metric_tile("performance_overview_stat_3", "Profit Factor", "1.12", 40, "primary")
                    metric_tile("performance_overview_stat_4", "Account Age", "152 days", 40, "primary")
                    metric_tile("performance_overview_stat_5", "Most Traded Symbol", "XAUUSD", 40, "primary")

                st.divider()

                # ------ TRADE EFFICIENCY ------ #
            
                st.subheader("Trade Efficiency", anchor=False)
                st.caption("Evaluate the effectiveness and precision of recent trades based on set metrics.")

                chart, stats = st.columns([3, 1], vertical_alignment="bottom")

                with chart:
                    with tile("trade_efficiency_chart", 385):
                        st.markdown("**Chart**")

                with stats:
                    metric_tile("performance_efficiency_stat_1", "Stat 1", "00.00%", 40, "primary")
                    metric_tile("performance_efficiency_stat_2", "Stat 2", "00.00%", 40, "primary")
                    metric_tile("performance_efficiency_stat_3", "Stat 3", "00.00%", 40, "primary")
                    metric_tile("performance_efficiency_stat_4", "Stat 4", "00.00%", 40, "primary")
                    metric_tile("performance_efficiency_stat_5", "Stat 5", "00.00%", 40, "primary")

                st.divider()

                # ------ RISK ANALYSIS ------ #
            
                st.subheader("Risk Analysis", anchor=False)
                st.caption("Assess trading risks and operational efficiency to optimize risk management strategies.")

                chart, stats = st.columns([3, 1], vertical_alignment="bottom")

                with chart:
                    with tile("risk_analysis_chart", 385):
                        st.markdown("**Chart**")

                with stats:
                    metric_tile("performance_risk_stat_1", "Stat 1", "00.00%", 40, "primary")
                    metric_tile("performance_risk_stat_2", "Stat 2", "00.00%", 40, "primary")
                    metric_tile("performance_risk_stat_3", "Stat 3", "00.00%", 40, "primary")
                    metric_tile("performance_risk_stat_4", "Stat 4", "00.00%", 40, "primary")
                    metric_tile("performance_risk_stat_5", "Stat 5", "00.00%", 40, "primary")

                st.divider()

                # ------ BEHAVIOURAL PATTERNS ------ #
            
                st.subheader("Behavioural Patterns", anchor=False)
                st.caption("Identify trends in trading behavior that impact performance outcomes.")

                chart, stats = st.columns([3, 1], vertical_alignment="bottom")

                with chart:
                    with tile("behavioural_patterns_chart", 385):
                        st.markdown("**Chart**")

                with stats:
                    metric_tile("performance_risk_stat_1", "Stat 1", "00.00%", 40, "primary")
                    metric_tile("performance_risk_stat_2", "Stat 2", "00.00%", 40, "primary")
                    metric_tile("performance_risk_stat_3", "Stat 3", "00.00%", 40, "primary")
                    metric_tile("performance_risk_stat_4", "Stat 4", "00.00%", 40, "primary")
                    metric_tile("performance_risk_stat_5", "Stat 5", "00.00%", 40, "primary")

                st.divider()

                # ------ MARKET CONDITION ANALYSIS ------ #
            
                st.subheader("Market Condition Analysis", anchor=False)
                st.caption("Analyse how different market conditions influence trade decisions and results.")

                chart, stats = st.columns([3, 1], vertical_alignment="bottom")

                with chart:
                    with tile("market_condition_chart", 385):
                        st.markdown("**Chart**")

                with stats:
                    metric_tile("performance_market_stat_1", "Stat 1", "00.00%", 40, "primary")
                    metric_tile("performance_market_stat_2", "Stat 2", "00.00%", 40, "primary")
                    metric_tile("performance_market_stat_3", "Stat 3", "00.00%", 40, "primary")
                    metric_tile("performance_market_stat_4", "Stat 4", "00.00%", 40, "primary")
                    metric_tile("performance_market_stat_5", "Stat 5", "00.00%", 40, "primary")

                st.divider()

                # ------ DAILY/WEEKLY PERFORMANCE SUMMARY ------ #
            
                st.subheader("Daily/Weekly Performance Summary", anchor=False)
                st.caption("Summary of performance metrics over daily and weekly intervals for tracking progress and trends.")

                chart, stats = st.columns([3, 1], vertical_alignment="bottom")

                with chart:
                    with tile("daily_weekly_summary_chart", 385):
                        st.markdown("**Chart**")

                with stats:
                    metric_tile("performance_summary_stat_1", "Stat 1", "00.00%", 40, "primary")
                    metric_tile("performance_summary_stat_2", "Stat 2", "00.00%", 40, "primary")
                    metric_tile("performance_summary_stat_3", "Stat 3", "00.00%", 40, "primary")
                    metric_tile("performance_summary_stat_4", "Stat 4", "00.00%", 40, "primary")
                    metric_tile("performance_summary_stat_5", "Stat 5", "00.00%", 40, "primary")

        else:
            st.info("No Account Selected")

def systems_page():
    with st.container(border=False):
        gradient_text("Systems", "2em")

def settings_page():
    with st.container(border=False):
        gradient_text("Settings", "2em")

def logout_page():
    gradient_text("Logout", "2em")

# Define pages as a dictionary of page groups and individual pages
pages = {
    "Home": [
        st.Page(dashboard_page, title="Dashboard", icon=":material/dashboard:"),
        st.Page(accounts_page, title="My Accounts", icon=":material/group:"),
        st.Page(systems_page, title="Systems", icon=":material/ssid_chart:"),
    ],
    "Settings": [
        st.Page(settings_page, title="Settings", icon=":material/settings:"),
        st.Page(logout_page, title="Logout", icon=":material/logout:"),
    ],
}

with st.sidebar:
    with st.container(border=True):
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

        gradient_text("Limited lifetime deal ends soon!", "1em")

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

        st.markdown("")

    st.caption('''
                Created with ❤️ by [Black Box Research](https://blackboxresearch.com/).
                ''')


# Set up the navigation
pg = st.navigation(pages, position="sidebar")
pg.run()
