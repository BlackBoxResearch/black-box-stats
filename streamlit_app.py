import streamlit as st
import hashlib
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.switch_page_button import switch_page
import time
import asyncio
from utils import api
import pandas as pd
import datetime as dt
import altair as alt
from vega_datasets import data
from st_aggrid import AgGrid, GridOptionsBuilder
st.set_page_config(layout="wide")

now = dt.datetime.utcnow()
current_time = now.hour + now.minute / 60  # Convert to hour with decimal minutes

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
            result = s.execute(query, params or {})
            return result.fetchall()
        except Exception as e:
            st.error(f"Error executing query: {e}")
            return []

def execute_write(query, params=None):
    """
    Executes a write SQL query (INSERT, UPDATE, DELETE) and commits the transaction.
    Args:
        query (str): The SQL query to execute.
        params (dict): Parameters for the query, if any.
    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    conn = st.connection('analytiq_db', type='sql')
    with conn.session as s:
        try:
            s.execute(query, params or {})
            s.commit()
            return True
        except Exception as e:
            st.error(f"Error executing write query: {e}")
            return False

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_login(email, password):
    """
    Checks if the login credentials are valid.
    Args:
        email (str): The email of the user.
        password (str): The password entered by the user.
    Returns:
        tuple: User details (user_id, email, first_name, last_name, subscription_level) if login is successful,
               otherwise a tuple of None values.
    """
    # Query to get user details by email
    query = '''
        SELECT user_id, email, first_name, last_name, subscription_level, password_hash
        FROM users
        WHERE email = :email
    '''

    # Execute the query using the helper function
    result = execute_query(query, {'email': email})

    # If a user is found
    if result:
        user_id, email, first_name, last_name, subscription_level, password_hash = result[0]
        print(f"User found: {email}, {first_name}, {subscription_level}")
        print(f"Stored hash: {password_hash}")
        print(f"Computed hash: {hash_password(password)}")

        # Validate the password
        if hash_password(password) == password_hash:
            return user_id, email, first_name, last_name, subscription_level

    # If login fails, return None values
    return None, None, None, None, None

def register_user(first_name, last_name, email, country, password, password_hint):
    """
    Registers a new user in the database.
    Args:
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The user's email address.
        country (str): The user's country.
        password (str): The user's password.
        password_hint (str): A hint for the password.
    Returns:
        bool: True if registration is successful, False otherwise.
    """
    # Check if the email already exists
    query_check = '''
        SELECT email FROM users WHERE email = :email
    '''
    existing_user = execute_query(query_check, {'email': email})

    if existing_user:
        st.error("User already exists. Please use a different email.")
        return False

    # Insert the new user
    password_hash = hash_password(password)
    query_insert = '''
        INSERT INTO users (first_name, last_name, email, country, password_hash, password_hint)
        VALUES (:first_name, :last_name, :email, :country, :password_hash, :password_hint)
    '''
    params = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'country': country,
        'password_hash': password_hash,
        'password_hint': password_hint
    }

    if execute_write(query_insert, params):
        st.success("Registration successful! You can now log in with your credentials.")
        return True
    else:
        st.error("An error occurred while trying to register the user. Please try again.")
        return False

def create_navigation(pages):
    # Create the navigation sidebar
    selected_page = st.navigation(pages, position="sidebar")
    # Run the selected page function
    selected_page.run()

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

async def FetchStatsFragment(api_account_id, account_id, user_id, login):
    # Fetch stats and trades for the selected account
    await api.FetchStats(api_account_id, account_id, user_id, login)

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

## LOGIN PAGE ##
def LoginPage():
    countries = [
        "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia",
        "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium",
        "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria",
        "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad",
        "Chile", "China", "Colombia", "Comoros", "Congo, Democratic Republic of the", "Congo, Republic of the",
        "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica",
        "Dominican Republic",
        "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji",
        "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala",
        "Guinea",
        "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq",
        "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea, North",
        "Korea, South", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya",
        "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta",
        "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia",
        "Montenegro", "Morocco", "Mozambique", "Myanmar (Burma)", "Namibia", "Nauru", "Nepal", "Netherlands",
        "New Zealand",
        "Nicaragua", "Niger", "Nigeria", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Panama",
        "Papua New Guinea",
        "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda",
        "Saint Kitts and Nevis",
        "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe",
        "Saudi Arabia",
        "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands",
        "Somalia",
        "South Africa", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan",
        "Tajikistan",
        "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey",
        "Turkmenistan",
        "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay",
        "Uzbekistan",
        "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
    ]

    @st.dialog("Register New Account")
    def open_register_dialog():
        with st.form("register_form", border=False):
            col1, col2 = st.columns(2)
            first_name = col1.text_input("First name")
            last_name = col2.text_input("Last name")
            email = col1.text_input("Email")
            country = col2.selectbox("Country", countries)
            password = col1.text_input("Password", type="password")
            repeat_password = col2.text_input("Repeat password", type="password")
            password_hint = st.text_input("Password hint")
            marketing_preferences = st.checkbox("Opt out of communications")
            terms_and_conditions = st.checkbox("I agree to the Terms of Use")

            if st.form_submit_button("Register", use_container_width=True, type='primary'):
                if password != repeat_password:
                    st.error("Passwords do not match.")
                elif not first_name or not last_name or not email or not password:
                    st.error("All fields are required.")
                else:
                    register_user(first_name, last_name, email, country, password, password_hint)

    @st.dialog("Sign In")
    def open_sign_in_dialog():
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        with stylable_container(
                # border: 1px solid #434343;
                key="sign_in_confirm_button",
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
            if st.button("Sign in", use_container_width=True):
                user_id, email, first_name, last_name, subscription_level = check_login(email, password)
                if email:
                    # Reset the logged_out state when logging in successfully
                    st.session_state["logged_out"] = False
                    st.session_state["logged_in"] = True
                    st.session_state["user_id"] = user_id
                    st.session_state["first_name"] = first_name
                    st.session_state["last_name"] = last_name
                    st.session_state["email"] = email
                    st.session_state["subscription_level"] = subscription_level

                    st.success(f"Logged in successfully as {first_name}!")

                    st.rerun()
                else:
                    st.error("Incorrect email or password. Please try again.")

    with stylable_container(
            key="login_container",
            css_styles="""
            {
                width: 500px;
                margin: 0 auto; /* Center the container */
            }
            """,
    ):
        with st.container(border=False):
            # Custom CSS to align elements
            st.markdown(
                """
                <style>
                .subheader {
                    text-align: center;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            st.image("static/BBS_type_logo.png")
            # Add vertical space
            st.write("")
            st.write("")
            st.write("")

            if st.button("Sign in", key="open_sign_in_dialog", use_container_width=True, type="secondary"):
                open_sign_in_dialog()

            st.markdown("""
                    <div style="display: flex; align-items: center;">
                        <hr style="flex-grow: 1; border: 1px solid #e8e8e8;">
                        <span style="margin: 0 10px;">or</span>
                        <hr style="flex-grow: 1; border: 1px solid #e8e8e8;">
                    </div>
                    """, unsafe_allow_html=True)

            # Register button to open the registration dialog

            with stylable_container(
                    # border: 1px solid #434343;
                    key="register_button",
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
                if st.button("Register for free", use_container_width=True):
                    open_register_dialog()

            st.caption("By signing up, you agree to the Terms of Service and Privacy Policy, including Cookie Use.")

## DASHBOARD PAGE ##
def DashboardPage():
    with stylable_container(
            key="main_container",
            css_styles="""
        {
            width: 1000px;
            margin: 0 auto; /* Center the container */
        }
        """,
    ):
        with st.container(border=False):
            first_name = st.session_state.get("first_name", "User")
            user_id = st.session_state.get("user_id", "User")

            st.title(f"Welcome back, {first_name}!", anchor=False)
            st.caption("Take a look at your latest performance metrics")

            col1, col2, col3, col4 = st.columns(4, vertical_alignment="bottom")

            with col1:
                with gradient_tile("dashboard_plan_card"):
                    with st.container(border=False, height=55):
                        st.markdown(
                            """
                            <div style="line-height: 1.4;">
                                <p style="margin: 0; font-size: 0.9em; color: #171717;">Plan</p>
                                <p style="margin: 0; font-size: 1.5em; font-weight: bold; color: #171717;">Pro</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

            with col2:
                with tile("dashboard_stat_1"):
                    with st.container(border=False, height=55):
                        st.markdown(
                            """
                            <div style="line-height: 1.4;">
                                <p style="margin: 0; font-size: 0.9em;">Stat 1</p>
                                <p style="margin: 0; font-size: 1.5em; font-weight: bold;">Value</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

            with col3:
                with tile("dashboard_stat_2"):
                    with st.container(border=False, height=55):
                        st.markdown(
                            """
                            <div style="line-height: 1.4;">
                                <p style="margin: 0; font-size: 0.9em;">Stat 2</p>
                                <p style="margin: 0; font-size: 1.5em; font-weight: bold;">Value</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

            with col4:
                with tile("dashboard_stat_3"):
                    with st.container(border=False, height=55):
                        st.markdown(
                            """
                            <div style="line-height: 1.4;">
                                <p style="margin: 0; font-size: 0.9em;">Stat 3</p>
                                <p style="margin: 0; font-size: 1.5em; font-weight: bold;">Value</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

            st.divider()

            col1, col2 = st.columns([2.5,1], vertical_alignment="bottom")
            with col1:
                with tile("session_map"):
                    with st.container(border=False, height=460):
                        st.markdown("**Trading Session**")

                        # Source of land data
                        source = alt.topo_feature(data.world_110m.url, 'countries')

                        # Base map with adjusted projection to crop empty areas
                        map_chart = alt.Chart(source).mark_geoshape(
                            fill='#adadad', stroke='#171717'
                        ).transform_filter(
                            "datum.id != '010'"  # Exclude Antarctica
                        ).project(
                            'naturalEarth1',  # Projection
                            scale=150,  # Adjust scale to zoom in and crop
                            translate=[300, 200]  # Center map horizontally and vertically
                        )

                        # Vertical line for current time (hour + minutes)
                        time_line = alt.Chart(pd.DataFrame({'current_time': [current_time]})).mark_rule(
                            color='#94B9FF', strokeWidth=2
                        ).encode(
                            x=alt.X('current_time:Q', title="Current Time (UTC)", scale=alt.Scale(domain=(23, 0))),
                            tooltip=[alt.Tooltip('current_time:Q', title='Current Time', format='.2f')]
                        )

                        # Combine map and vertical line
                        chart = alt.layer(map_chart, time_line).properties(
                            height=400, width=800, background='#171717',
                            padding={"top": 0, "bottom": 0, "left": 10, "right": 10}
                        ).configure_view(
                            stroke=None

                        )

                        # Display chart
                        st.altair_chart(chart, use_container_width=True)

            with col2:
                with tile("clock"):
                    with st.container(border=False, height=460):
                        st.markdown("Clock")

## ACCOUNTS PAGE ##
def AccountsPage():
    with stylable_container(
            key="main_container",
            css_styles="""
        {
            width: 1000px;
            margin: 0 auto; /* Center the container */
        }
        """,
    ):
        with st.container(border=False):
            user_id = st.session_state.get("user_id", "User")

            st.title(f"My Accounts", anchor=False)

            # +------------------------------------------------------------------------------------------------+

            # Get the list of account numbers for the user
            account_numbers = get_user_accounts(user_id)

            # Prepare the account number options for the selectbox
            if account_numbers:
                account_options = account_numbers
            else:
                account_options = ["No accounts available"]
            col1, col2, col3, col4 = st.columns(4, vertical_alignment="bottom")

            # Create the selectbox with the retrieved account number options
            with col1:
                account_selection = st.selectbox(
                    "Select Account",
                    account_options
                )

            with col2:
                @st.dialog("Add Account")
                def add_account_dialog():
                    account_number = st.text_input("Account Number", placeholder="Account Number")
                    password = st.text_input("Investor Password", placeholder="Investor Password", type="password")
                    server = st.text_input("Server", placeholder="Server")
                    platform = st.selectbox("Platform", ("mt4", "mt5"), placeholder="Platform")

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
                        confirm_add_account_button = st.button("Add Account", icon=":material/check:",
                                                               use_container_width=True)

                    if confirm_add_account_button:
                        # Use a spinner to indicate loading
                        with st.spinner("Adding your account..."):
                            # Run the async function and get the result
                            api_account_id, account_name, error_message = asyncio.run(
                                api.AddAccount(user_id, account_number, password, server, platform)
                            )

                            # Display success or error messages based on the result
                            if api_account_id:
                                st.success(
                                    f"Account '{account_name}' added successfully!")
                                time.sleep(2)
                                st.rerun()
                            else:
                                # Display the specific error message returned by AddAccount
                                if error_message:
                                    st.error(error_message)
                                else:
                                    st.error("Failed to add account. Please check your inputs and try again.")

                with stylable_container(
                        # border: 1px solid #434343;
                        key="add_account_button",
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
                    open_add_account_dialog = st.button("Add Account", icon=":material/add_circle:",
                                                        use_container_width=True)

                if open_add_account_dialog: add_account_dialog()

            # +------------------------------------------------------------------------------------------------+

            # Check if an account is selected (ensure account_selection is not "No accounts available")
            if account_selection and account_selection != "No accounts available":
                # Query the database to get the `api_account_id` and `account_id` for the selected account
                conn = st.connection('analytiq_db', type='sql')
                with conn.session as s:
                    account_info = s.execute(
                        '''
                        SELECT api_account_id, account_id
                        FROM accounts
                        WHERE user_id = :user_id AND account_number = :account_number
                        ''',
                        {'user_id': user_id, 'account_number': account_selection}
                    ).fetchone()

                # Check if an account is selected (ensure account_selection is not "No accounts available")
                if account_info:
                    api_account_id, account_id = account_info

                    with conn.session as s:
                        # Retrieve trades for the specific account
                        query = '''
                            SELECT close_time, profit, gain, duration_mins
                            FROM trades
                            WHERE api_account_id = :api_account_id
                        '''
                        result = s.execute(query, {'api_account_id': api_account_id}).fetchall()

                    # Convert the result into a DataFrame
                    trades_df = pd.DataFrame(result, columns=['close_time', 'profit', 'gain', 'duration_mins'])
                    trades_df['close_time'] = pd.to_datetime(trades_df['close_time'])
                    trades_df['cum_gain'] = trades_df['gain'].cumsum()

                    if trades_df.empty:
                        st.info("No trading data available.")
                    else:
                        tab1, tab2, tab3, tab4, tab5 = st.tabs(
                            ["Performance", "Trade Journal", "Analytic Tools", "AI Insights", "Settings"])

                        with tab1:
                            title, col2, periods = st.columns([2, 0.2, 1], vertical_alignment="bottom")

                            # ------ OVERVIEW STATS ------ #

                            title.subheader("Overview", anchor=False)
                            title.caption(f"General performance overview for account {account_selection}.")

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
                                    with st.container(border=False, height=460):
                                        st.markdown("**Gain/Time**")

                                        # Calculate rolling 5% VaR (5th percentile) with a window of 10 periods
                                        window_size = 10

                                        # Set close_time as the index and prepare the line_data DataFrame
                                        line_data = trades_df[['close_time', 'cum_gain']].set_index('close_time')
                                        line_data['VaR'] = line_data['cum_gain'].rolling(window=window_size).quantile(
                                            0.05)
                                        line_data.reset_index(inplace=True)  # Reset index to make 'close_time' a column

                                        # Ensure 'close_time' is interpreted as a datetime by Altair
                                        line_data['close_time'] = pd.to_datetime(line_data['close_time'])

                                        # Create the main line chart with a gradient fill
                                        line_chart = alt.Chart(line_data).mark_area(
                                            line={'color': '#94b9ff'},  # Line color
                                            color=alt.Gradient(  # Gradient fill with specified opacity
                                                gradient='linear',
                                                stops=[alt.GradientStop(color='rgba(148, 185, 255, 0.5)', offset=0),
                                                       alt.GradientStop(color='rgba(148, 185, 255, 0)', offset=1)],
                                                x1=1, x2=1, y1=1, y2=0
                                            ),
                                            interpolate='monotone'  # Smooth the line
                                        ).encode(
                                            x=alt.X('close_time:T', title='Time'),
                                            # Specify quantitative data type
                                            y=alt.Y('cum_gain:Q', title='Cumulative Gain (%)')
                                            # Specify quantitative data type
                                        )

                                        # Create the rolling VaR line
                                        var_line = alt.Chart(line_data).mark_line(
                                            color='yellow',  # Yellow color for the VaR line
                                            strokeDash=[4, 4],  # Dotted line
                                            strokeWidth=1  # 1px thickness
                                        ).encode(
                                            x='close_time:T',
                                            y='VaR:Q'
                                        )
                                        # Combine the main chart and VaR line
                                        combined_chart = (line_chart + var_line).properties(
                                            height=410,  # Set the height of the chart
                                            background='#171717'  # Background color
                                        ).configure_axis(
                                            grid=False  # Remove grid lines
                                        ).configure_view(
                                            strokeWidth=0  # Remove borders around the chart
                                        )

                                        st.altair_chart(combined_chart, use_container_width=True)

                            with stats:
                                with gradient_tile("performance_overview_stat_1"):
                                    with st.container(border=False, height=55):
                                        st.markdown(
                                            """
                                            <div style="line-height: 1.4;">
                                                <p style="margin: 0; font-size: 0.9em; color: #171717;">AnalytiQ Score</p>
                                                <p style="margin: 0; font-size: 1.5em; font-weight: bold; color: #171717;">78</p>
                                            </div>
                                            """,
                                            unsafe_allow_html=True
                                        )

                                with tile("performance_overview_stat_2"):
                                    with st.container(border=False, height=55):
                                        st.markdown(
                                            """
                                            <div style="line-height: 1.4;">
                                                <p style="margin: 0; font-size: 0.9em; color: #FFFFFF;">Win Rate</p>
                                                <p style="margin: 0; font-size: 1.5em; font-weight: bold; color: #FFFFFF;">67.21%</p>
                                            </div>
                                            """,
                                            unsafe_allow_html=True
                                        )

                                with tile("performance_overview_stat_3"):
                                    with st.container(border=False, height=55):
                                        st.markdown(
                                            """
                                            <div style="line-height: 1.4;">
                                                <p style="margin: 0; font-size: 0.9em; color: #FFFFFF;">Profit Factor</p>
                                                <p style="margin: 0; font-size: 1.5em; font-weight: bold; color: #FFFFFF;">1.12</p>
                                            </div>
                                            """,
                                            unsafe_allow_html=True
                                        )

                                with tile("performance_overview_stat_4"):
                                    with st.container(border=False, height=55):
                                        st.markdown(
                                            """
                                            <div style="line-height: 1.4;">
                                                <p style="margin: 0; font-size: 0.9em; color: #FFFFFF;">Average Win/Loss</p>
                                                <p style="margin: 0; font-size: 1.5em; font-weight: bold; color: #FFFFFF;">1.53</p>
                                            </div>
                                            """,
                                            unsafe_allow_html=True
                                        )

                                with tile("performance_overview_stat_5"):
                                    with st.container(border=False, height=55):
                                        st.markdown(
                                            """
                                            <div style="line-height: 1.4;">
                                                <p style="margin: 0; font-size: 0.9em; color: #FFFFFF;">Most Traded Symbol</p>
                                                <p style="margin: 0; font-size: 1.5em; font-weight: bold; color: #FFFFFF;">XAUUSD</p>
                                            </div>
                                            """,
                                            unsafe_allow_html=True
                                        )

                            # ------ TRADE EFFICIENCY STATS ------ #

                            st.divider()
                            st.subheader("Trade Efficiency", anchor=False)
                            st.caption(
                                "Evaluate the effectiveness and precision of recent trades based on set metrics.")

                            chart, stats = st.columns([3, 1], vertical_alignment="bottom")

                            with chart:
                                with tile("profit_duration_chart"):
                                    with st.container(border=False, height=460):
                                        st.markdown("**Profit vs Duration**")
                                        scatter_chart = alt.Chart(trades_df).mark_circle(
                                            size=60,  # Size of the points
                                            color='#94b9ff',  # Solid blue color
                                            opacity=0.7  # Set overall opacity of points
                                        ).encode(
                                            x=alt.X('duration_mins:Q', title='Trade Duration (minutes)'),
                                            # Specify quantitative data type
                                            y=alt.Y('gain:Q', title='Trade Gain (%)')
                                            # Specify quantitative data type
                                        )

                                        # Trendline layer
                                        trendline = alt.Chart(trades_df).transform_regression(
                                            'duration_mins', 'gain'  # Specify the x and y for regression
                                        ).mark_line(
                                            color='yellow',  # Yellow color for the VaR line
                                            strokeDash=[4, 4],  # Dotted line
                                            strokeWidth=1  # 1px thickness
                                        ).encode(
                                            x='duration_mins:Q',
                                            y='gain:Q'
                                        )

                                        # Combine scatter plot and trendline
                                        combined_chart = (scatter_chart + trendline).properties(
                                            height=410,  # Set the height of the chart
                                            background='#171717'  # Background color
                                        ).configure_axis(
                                            grid=False  # Remove grid lines
                                        ).configure_view(
                                            strokeWidth=0  # Remove borders around the chart
                                        )

                                        # Display the chart in Streamlit
                                        st.altair_chart(combined_chart, use_container_width=True)

                            with stats:
                                with tile("trade_efficiency_stat_1"):
                                    with st.container(border=False, height=55):
                                        st.markdown(
                                            """
                                            <div style="line-height: 1.4;">
                                                <p style="margin: 0; font-size: 0.9em; color: #FFFFFF;">Average Win Duration</p>
                                                <p style="margin: 0; font-size: 1.5em; font-weight: bold; color: #FFFFFF;">121 mins</p>
                                            </div>
                                            """,
                                            unsafe_allow_html=True
                                        )

                                with tile("trade_efficiency_stat_2"):
                                    with st.container(border=False, height=55):
                                        st.markdown(
                                            """
                                            <div style="line-height: 1.4;">
                                                <p style="margin: 0; font-size: 0.9em; color: #FFFFFF;">Average Loss Duration</p>
                                                <p style="margin: 0; font-size: 1.5em; font-weight: bold; color: #FFFFFF;">276 mins</p>
                                            </div>
                                            """,
                                            unsafe_allow_html=True
                                        )

                                with tile("trade_efficiency_stat_3"):
                                    with st.container(border=False, height=55):
                                        st.markdown(
                                            """
                                            <div style="line-height: 1.4;">
                                                <p style="margin: 0; font-size: 0.9em; color: #FFFFFF;">Consistency (Std Dev)</p>
                                                <p style="margin: 0; font-size: 1.5em; font-weight: bold; color: #FFFFFF;">1.21</p>
                                            </div>
                                            """,
                                            unsafe_allow_html=True
                                        )

                                with tile("trade_efficiency_stat_4"):
                                    with st.container(border=False, height=55):
                                        st.markdown(
                                            """
                                            <div style="line-height: 1.4;">
                                                <p style="margin: 0; font-size: 0.9em; color: #FFFFFF;">Avg Win Streak</p>
                                                <p style="margin: 0; font-size: 1.5em; font-weight: bold; color: #FFFFFF;">2</p>
                                            </div>
                                            """,
                                            unsafe_allow_html=True
                                        )

                                with tile("trade_efficiency_stat_5"):
                                    with st.container(border=False, height=55):
                                        st.markdown(
                                            """
                                            <div style="line-height: 1.4;">
                                                <p style="margin: 0; font-size: 0.9em; color: #FFFFFF;">Avg Loss Streak</p>
                                                <p style="margin: 0; font-size: 1.5em; font-weight: bold; color: #FFFFFF;">3</p>
                                            </div>
                                            """,
                                            unsafe_allow_html=True
                                        )

                            # ------ RISK AND EFFICIENCY STATS ------ #

                            st.divider()
                            st.subheader("Risk and Efficiency Analysis", anchor=False)
                            st.caption("Assess trading risks and operational efficiency to optimize risk management strategies.")

                            chart, stats = st.columns([3, 1], vertical_alignment="bottom")

                            with chart:
                                with tile("profit_drawdown_chart"):
                                    with st.container(border=False, height=460):
                                        st.markdown("**Profit vs. Drawdown Chart**")

                            with stats:
                                with tile("performance_risk_stat_1"):
                                    with st.container(border=False, height=55):
                                        st.markdown(
                                            """
                                            <div style="line-height: 1.4;">
                                                <p style="margin: 0; font-size: 0.9em; color: #FFFFFF;">Sharpe Ratio</p>
                                                <p style="margin: 0; font-size: 1.5em; font-weight: bold; color: #FFFFFF;">1.12</p>
                                            </div>
                                            """,
                                            unsafe_allow_html=True
                                        )

                                with tile("performance_risk_stat_2"):
                                    with st.container(border=False, height=55):
                                        st.markdown(
                                            """
                                            <div style="line-height: 1.4;">
                                                <p style="margin: 0; font-size: 0.9em; color: #FFFFFF;">Max Drawdown</p>
                                                <p style="margin: 0; font-size: 1.5em; font-weight: bold; color: #FFFFFF;">12.39%</p>
                                            </div>
                                            """,
                                            unsafe_allow_html=True
                                        )

                                with tile("performance_risk_stat_3"):
                                    with st.container(border=False, height=55):
                                        st.markdown(
                                            """
                                            <div style="line-height: 1.4;">
                                                <p style="margin: 0; font-size: 0.9em; color: #FFFFFF;">Return/Max Drawdown</p>
                                                <p style="margin: 0; font-size: 1.5em; font-weight: bold; color: #FFFFFF;">1.21</p>
                                            </div>
                                            """,
                                            unsafe_allow_html=True
                                        )

                                with tile("performance_risk_stat_4"):
                                    with st.container(border=False, height=55):
                                        st.markdown(
                                            """
                                            <div style="line-height: 1.4;">
                                                <p style="margin: 0; font-size: 0.9em; color: #FFFFFF;">Avg Drawdown Duration</p>
                                                <p style="margin: 0; font-size: 1.5em; font-weight: bold; color: #FFFFFF;">1.58 Days</p>
                                            </div>
                                            """,
                                            unsafe_allow_html=True
                                        )

                                with tile("performance_risk_stat_5"):
                                    with st.container(border=False, height=55):
                                        st.markdown(
                                            """
                                            <div style="line-height: 1.4;">
                                                <p style="margin: 0; font-size: 0.9em; color: #FFFFFF;">Recovery Factor</p>
                                                <p style="margin: 0; font-size: 1.5em; font-weight: bold; color: #FFFFFF;">1.20</p>
                                            </div>
                                            """,
                                            unsafe_allow_html=True
                                        )



                            # ------ BEHAVIOURAL PATTERNS ------ #

                            st.divider()
                            st.subheader("Behavioural Patters", anchor=False)
                            st.caption("Identify trends in trading behavior that impact performance outcomes.")

                            # ------ MARKET CONDITION ANALYSIS ------ #

                            st.divider()
                            st.subheader("Market Condition Analysis", anchor=False)
                            st.caption("Analyse how different market conditions influence trade decisions and results.")

                            # ------ DAILY/WEEKLY SUMMARY ------ #

                            st.divider()
                            st.subheader("Daily / Weekly Performance Summary", anchor=False)
                            st.caption("Summary of performance metrics over daily and weekly intervals for tracking progress and trends.")

                        with tab2:  # Trade Journal tab
                            st.subheader("Trade Journal", anchor=False)

                            if trades_df.empty:
                                st.info("No trading data available.")
                            else:
                                # Query the database to get the trades for the selected account
                                with conn.session as s:
                                    result = s.execute(
                                        '''
                                        SELECT ticket, symbol, type, volume, open_time, open_price, close_time, close_price, profit, pips, gain, success, duration_mins
                                        FROM trades
                                        WHERE user_id = :user_id AND account_id = :account_id
                                        ''',
                                        {'user_id': user_id, 'account_id': account_id}
                                    )

                                    # Fetch all rows and convert them into a DataFrame
                                    trades_data = result.fetchall()

                                    trades_df = pd.DataFrame(trades_data, columns=[
                                        'ticket', 'symbol', 'type', 'volume', 'open_time', 'open_price',
                                        'close_time', 'close_price', 'profit', 'pips', 'gain', 'success',
                                        'duration_mins'
                                    ])

                                    # Add an "id" column to ensure each row has a unique identifier
                                    trades_df['id'] = trades_df['ticket']

                                    # Drop the 'ticket' column
                                    trades_df.drop(['ticket'], axis=1, inplace=True)

                                    # Convert open_time to datetime
                                    trades_df['open_time'] = pd.to_datetime(trades_df['open_time'])
                                    trades_df['close_time'] = pd.to_datetime(trades_df['close_time'])

                                    # Format open_time to "dd/mm/yy hh:mm:ss"
                                    trades_df['open_time'] = trades_df['open_time'].dt.strftime('%d/%m/%Y %H:%M:%S')
                                    trades_df['close_time'] = trades_df['close_time'].dt.strftime('%d/%m/%Y %H:%M:%S')

                                    # Convert success column to boolean and datetime columns to string format for DataGrid compatibility
                                    trades_df['success'] = trades_df['success'].apply(
                                        lambda x: True if x == "won" else False)

                                    # Convert type column to Buy or Sell
                                    trades_df['type'] = trades_df['type'].apply(
                                        lambda x: "Sell" if x == "DEAL_TYPE_SELL" else "Buy")

                                # Convert trades_df to a list of dictionaries
                                rows = trades_df.to_dict(orient="records")

                        with tab5:
                            # Layout with 4 columns for settings
                            col1, col2, col3, col4 = st.columns(4)

                            # Display settings heading in the first column
                            with col1:
                                st.subheader("Settings", anchor=False)

                            # Display the Remove Account button in the fourth column
                            with col4:
                                @st.dialog("Remove Account")
                                def remove_account_dialog():
                                    st.write(f"Are you sure you want to remove account {account_selection}?")

                                    # Display confirmation buttons in a new row
                                    confirm_col1, confirm_col2 = st.columns(2)

                                    with confirm_col2:
                                        if st.button("No", type="primary", use_container_width=True):
                                            st.rerun()

                                    with confirm_col1:
                                        if st.button("Yes", type="secondary", use_container_width=True):
                                            with st.spinner("Removing your account..."):
                                                # Query the database to get the api_account_id
                                                conn = st.connection('analytiq_db', type='sql')
                                                with conn.session as s:
                                                    result = s.execute(
                                                        '''
                                                        SELECT api_account_id
                                                        FROM accounts
                                                        WHERE user_id = :user_id AND account_number = :account_number
                                                        ''',
                                                        {'user_id': user_id, 'account_number': account_selection}
                                                    )
                                                    api_account_id = result.scalar()

                                                # Run the async function to remove the account if it exists
                                                remove_account = asyncio.run(
                                                    api.RemoveAccount(api_account_id)) if api_account_id else False

                                            # Display success or error messages based on the result
                                            if remove_account:
                                                st.success(f"Account '{account_selection}' removed successfully!")
                                                time.sleep(2)
                                                st.rerun()
                                            elif remove_account is False:
                                                st.error(
                                                    "Failed to find the account. Please check the account number and try again.")
                                            else:
                                                st.error("Failed to remove account. Please try again.")

                                # Display the Remove Account button
                                open_remove_account_dialog = st.button(
                                    label="Remove Account",
                                    type="secondary",
                                    icon=":material/delete:",
                                    use_container_width=True
                                )

                                if open_remove_account_dialog:
                                    remove_account_dialog()

                else:
                    # Display "No account selected" in each tab if no account is selected
                    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Performance", "Trade Journal", "Settings"])

                    with tab1:
                        st.write("No account selected")

                    with tab2:
                        st.write("No account selected")

                    with tab3:
                        st.write("No account selected")

                    with tab4:
                        st.write("No account selected")


## SYSTEMS PAGE ##
def SystemsPage():
    with stylable_container(
            key="main_container",
            css_styles="""
        {
            width: 1000px;
            margin: 0 auto; /* Center the container */
        }
        """,
    ):
        with st.container(border=False):
            st.title("Systems")

            # Mock data
            data = {
                "System": ["Momentum Master", "Risk Reducer", "Alpha Tracker"],
                "Owner": ["Alice", "Bob", "Charlie"],
                "Subscribers": [150, 120, 95],
                "Monthly Fee ($)": [50, 40, 60],
                "Performance": [[0.02, 0.03, 0.05, -0.01], [-0.01, 0.02, 0.01, 0.03], [0.05, 0.04, -0.02, 0.03]],
                "System ID": [1, 2, 3],
            }

            df = pd.DataFrame(data)

            # Configure AgGrid with sparklines
            builder = GridOptionsBuilder.from_dataframe(
                df[["System", "Owner", "Subscribers", "Monthly Fee ($)", "Performance"]])

            # Configure the Sparkline column
            builder.configure_column(
                "Performance",
                header_name="Performance Chart",
                cellRenderer="agSparklineCellRenderer",
                cellRendererParams={
                    "sparklineOptions": {
                        "type": "line",
                        "marker": {"enabled": True},  # Optional: Add markers at data points
                        "tooltip": {"enabled": True},  # Enable tooltips for data points
                    }
                },
            )

            # Add button column for "Details"
            df["Details"] = df["System ID"]  # Pass the System ID for button functionality

            builder.configure_column(
                "Details",
                header_name="Details",
                cellRenderer='''function(params) {
                    return `<button onclick="window.open('https://yourapp.com/system/' + params.value, '_blank')">View</button>`;
                }''',
            )

            # Pagination and grid options
            builder.configure_pagination(enabled=True, paginationPageSize=10)
            grid_options = builder.build()

            # Display the leaderboard
            AgGrid(df, gridOptions=grid_options, allow_unsafe_jscode=True)


## SUPPORT PAGE ##
def SupportPage():
    st.title("Support")


## PROFILE PAGE ##
def ProfilePage():
    st.title("Profile")


## SETTINGS PAGE ##
def SettingsPage():
    st.title("Settings")


## SETTINGS PAGE ##
def SettingsPage():
    st.title("Settings")


## LOGOUT PAGE ##
def LogoutPage():
    # Function to create the logout dialog
    @st.dialog("Logout")
    def logout_dialog():
        st.write("Are you sure you want to log out?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Yes", type="secondary", use_container_width=True):
                st.session_state["logged_in"] = False
                st.session_state["logged_out"] = True
                st.success("Logged out successfully!")
                # Reset session state to prepare for next login
                st.session_state["logged_out"] = False
                st.rerun()
        with col2:
            if st.button("No", type="primary", use_container_width=True):
                switch_page("Dashboard")
                st.rerun()

    # Ensure session state variables are set
    if 'logged_out' not in st.session_state:
        st.session_state.logged_out = False

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = True

    # Show the logout dialog if the user is attempting to log out
    if st.session_state.logged_in and not st.session_state.logged_out:
        logout_dialog()

## SUBSCRIBE PAGE ##
def SubscribePage():
    st.title("Subscribe")

## MAIN FUNCTION ##
def main():
    # Check if user is already logged in
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    # Check if user has logged out and reset if necessary
    if "logged_out" not in st.session_state:
        st.session_state["logged_out"] = False

    # Display pages based on login state
    if st.session_state["logged_in"]:
        st.logo("static/BBS_type_logo.png", size="large", icon_image="static/icon.png")

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

        create_navigation(logged_in_pages)
    else:
        create_navigation(logged_out_pages)

# Define pages with icons
login_page = st.Page(page=LoginPage, title="Login", icon=":material/login:")
dashboard_page = st.Page(page=DashboardPage, title="Dashboard", icon=":material/dashboard:")
accounts_page = st.Page(page=AccountsPage, title="My Accounts", icon=":material/group:")
systems_page = st.Page(page=SystemsPage, title="Systems", icon=":material/stacked_line_chart:")
support_page = st.Page(page=SupportPage, title="Support", icon=":material/support_agent:")
profile_page = st.Page(page=ProfilePage, title="My Profile", icon=":material/account_circle:")
settings_page = st.Page(page=SettingsPage, title="Settings", icon=":material/settings:")
logout_page = st.Page(page=LogoutPage, title="Logout", icon=":material/logout:")
subscribe_page = st.Page(page=SubscribePage, title="Subscribe", icon=":material/upgrade:")

# Group pages for logged-out users
logged_out_pages = [login_page]

# Group pages for logged-in users
logged_in_pages = {
    "Home": [dashboard_page, accounts_page, systems_page],
    "Settings": [profile_page, settings_page, logout_page]  # Logout page added here
}






# Run the main function when the script is executed
if __name__ == "__main__":
    main()
