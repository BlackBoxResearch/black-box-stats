import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.bottom_container import bottom
from st_social_media_links import SocialMediaIcons
from sqlalchemy.sql import text
import time
import pandas as pd
import altair as alt

st.set_page_config(layout="centered")

st.logo(image="static/bbs_type_logo.png", size="large")    

def metric_tile(key, stat, value, height, type, tooltip):
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
                unsafe_allow_html=True, help=tooltip
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

def line_chart(data, x, y, x_label, y_label, height=280):
    """
    Generate a line chart with a gradient fill.
    
    Parameters:
        data (pd.DataFrame): The DataFrame containing the data to plot.
        x (str): The column name for the x-axis.
        y (str): The column name for the y-axis.
        x_label (str): The label for the x-axis.
        y_label (str): The label for the y-axis.
        height (int): The height of the chart. Default is 280.
    
    Returns:
        alt.Chart: The Altair chart object.
    """
    # Ensure the x-axis column is interpreted as datetime
    data[x] = pd.to_datetime(data[x])
    
    # Create the main line chart with a gradient fill
    chart = alt.Chart(data).mark_area(
        line={'color': '#94b9ff'},  # Line color
        color=alt.Gradient(  # Gradient fill with specified opacity
            gradient='linear',
            stops=[
                alt.GradientStop(color='rgba(148, 185, 255, 0.5)', offset=0),
                alt.GradientStop(color='rgba(148, 185, 255, 0)', offset=1)
            ],
            x1=1, x2=1, y1=1, y2=0
        ),
        interpolate='monotone'  # Smooth the line
    ).encode(
        x=alt.X(f'{x}:T', title=x_label),  # Specify temporal data type
        y=alt.Y(f'{y}:Q', title=y_label)  # Specify quantitative data type
    ).properties(
        height=height,  # Set the height of the chart
        background='#171717',  # Background color
        padding={"top": 10, "bottom": 10, "left": 10, "right": 10}
    ).configure_axis(
        grid=False  # Remove grid lines
    ).configure_view(
        strokeWidth=0  # Remove borders around the chart
    )
    
    return st.altair_chart(chart, use_container_width=True)

def scatter_chart(data, x, y, x_label, y_label, height=280):
    """
    Generate a scatter chart..
    
    Parameters:
        data (pd.DataFrame): The DataFrame containing the data to plot.
        x (str): The column name for the x-axis.
        y (str): The column name for the y-axis.
        x_label (str): The label for the x-axis.
        y_label (str): The label for the y-axis.
        height (int): The height of the chart. Default is 280.
    
    Returns:
        alt.Chart: The Altair chart object.
    """

    data[x]= pd.to_numeric(data[x], errors='coerce')
    
    # Create the main chart
    chart = alt.Chart(data).mark_circle(
                size=60,  # Size of the points
                color='#94b9ff',  # Solid blue color
                opacity=0.7  # Set overall opacity of points
    ).encode(
        x=alt.X(f'{x}:Q', title=x_label),  # Specify quantitative data type
        y=alt.Y(f'{y}:Q', title=y_label)  # Specify quantitative data type
    ).properties(
        height=height,  # Set the height of the chart
        background='#171717',  # Background color
        padding={"top": 10, "bottom": 10, "left": 10, "right": 10}
    ).configure_axis(
        grid=False  # Remove grid lines
    ).configure_view(
        strokeWidth=0  # Remove borders around the chart
    )
    
    return st.altair_chart(chart, use_container_width=True)

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

def get_account_info(user_id, account_number):
    """
    Fetch account information based on user_id and account_number.
    
    Args:
        user_id (int): The ID of the user.
        account_number (str): The account number.
        
    Returns:
        tuple: (api_account_id, account_id) if found, else None.
    """
    query = '''
        SELECT api_account_id, account_id
        FROM accounts
        WHERE user_id = :user_id AND account_number = :account_number
    '''
    
    result = execute_query(query, {'user_id': user_id, 'account_number': account_number})

    if result:  # Check if result contains any rows
        return result[0]  # Return the first row as a tuple
    else:
        return None  # Return None if no data found

def get_account_trades(api_account_id):
    """
    Fetch trades for a specific API account ID.
    
    Args:
        api_account_id (int): The API account ID for which to fetch trades.
        
    Returns:
        list: A list of tuples containing trade details, or an empty list if no trades found.
    """
    query = '''
        SELECT *
        FROM trades
        WHERE api_account_id = :api_account_id
    '''
    
    result = execute_query(query, {'api_account_id': api_account_id})
    
    if result:  # Check if there are any trades
        return result  # Return the raw result (list of tuples)
    else:
        return []  # Return an empty list if no trades are found

def calculate_trade_statistics(trades_df):
    """
    Calculate key statistics from the trade data.
    
    Args:
        trades_df (pd.DataFrame): DataFrame containing trade data.
    
    Returns:
        dict: Dictionary containing formatted key statistics.
    """
    # Ensure datetime columns are parsed correctly
    trades_df['open_time'] = pd.to_datetime(trades_df['open_time'])
    trades_df['close_time'] = pd.to_datetime(trades_df['close_time'])
    
    # Calculate Total Gain
    total_gain = trades_df['gain'].sum()
    
    # Calculate Win Rate
    total_trades = len(trades_df)
    winning_trades = trades_df[trades_df['success'] == 'won'].shape[0]
    win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
    
    # Calculate Profit Factor
    total_profit = trades_df[trades_df['profit'] > 0]['profit'].sum()
    total_loss = abs(trades_df[trades_df['profit'] < 0]['profit'].sum())
    profit_factor = (total_profit / total_loss) if total_loss > 0 else float('inf')
    
    # Calculate Account Age
    account_age_days = (trades_df['close_time'].max() - trades_df['open_time'].min()).days
    
    # Determine Most Traded Symbol
    most_traded_symbol = trades_df['symbol'].mode()[0] if not trades_df['symbol'].mode().empty else None
    
    # Calculate Trade Efficiency Stats
    avg_trade_duration = trades_df['duration_mins'].mean()
    avg_profit_per_trade = trades_df['profit'].mean()
    max_profit = trades_df['profit'].max()
    min_profit = trades_df['profit'].min()
    most_frequent_trade_type = trades_df['type'].mode()[0] if not trades_df['type'].mode().empty else None
    
    # Risk Analysis Stats
    max_drawdown = trades_df['cum_gain'].min()
    avg_risk_per_trade = trades_df[trades_df['profit'] < 0]['profit'].mean()
    sharpe_ratio = total_profit / trades_df['profit'].std() if trades_df['profit'].std() > 0 else float('inf')
    risk_reward_ratio = total_profit / abs(total_loss) if total_loss > 0 else float('inf')
    trades_at_risk = (len(trades_df[trades_df['profit'] < 0]) / total_trades) * 100 if total_trades > 0 else 0
    
    # Behavioural Patterns Stats
    most_frequent_symbol = trades_df['symbol'].mode()[0] if not trades_df['symbol'].mode().empty else None
    most_active_time = trades_df['open_time'].dt.hour.mode()[0] if not trades_df['open_time'].dt.hour.mode().empty else None
    avg_trade_volume = trades_df['volume'].mean()
    largest_volume_trade = trades_df['volume'].max()
    most_frequent_trade_outcome = trades_df['success'].mode()[0] if not trades_df['success'].mode().empty else None
    
    # Market Condition Stats
    best_symbol_profit = trades_df.groupby('symbol')['profit'].sum().idxmax() if not trades_df.empty else None
    worst_symbol_profit = trades_df.groupby('symbol')['profit'].sum().idxmin() if not trades_df.empty else None
    avg_profit_by_symbol = trades_df.groupby('symbol')['profit'].mean().to_dict()
    profit_volatility_by_symbol = trades_df.groupby('symbol')['profit'].std().to_dict()
    
    # Daily Aggregation
    trades_df['day'] = trades_df['close_time'].dt.date
    daily_profit = trades_df.groupby('day')['profit'].sum()
    best_day_profit = daily_profit.idxmax() if not daily_profit.empty else None
    worst_day_profit = daily_profit.idxmin() if not daily_profit.empty else None
    avg_daily_profit = daily_profit.mean()

    
    # Weekly Aggregation
    trades_df['week'] = trades_df['close_time'].dt.to_period('W').apply(lambda r: r.start_time)
    weekly_profit = trades_df.groupby('week')['profit'].sum()
    best_week_profit = weekly_profit.idxmax() if not weekly_profit.empty else None
    worst_week_profit = weekly_profit.idxmin() if not weekly_profit.empty else None

    # Compile results into a dictionary with formatting
    stats = {
        # Overview Stats
        "Total Gain": f"{total_gain:.2f}%",
        "Win Rate": f"{win_rate:.2f}%",
        "Profit Factor": f"{profit_factor:.2f}",
        "Account Age": f"{account_age_days} days",
        "Most Traded Symbol": most_traded_symbol,
        # Trade Efficiency
        "Avg Trade Duration": f"{avg_trade_duration:.2f} mins",
        "Avg Profit Per Trade": f"{avg_profit_per_trade:.2f}",
        "Max Profit": f"{max_profit:.2f}",
        "Min Profit": f"{min_profit:.2f}",
        "Most Frequent Type": most_frequent_trade_type,
        # Risk Analysis
        "Max Drawdown": f"{max_drawdown:.2f}",
        "Avg Risk Per Trade": f"{avg_risk_per_trade:.2f}",
        "Sharpe Ratio": f"{sharpe_ratio:.2f}",
        "Risk Reward Ratio": f"{risk_reward_ratio:.2f}",
        "Trades at Risk": f"{trades_at_risk:.2f}%",
        # Behavioural Patterns
        "Most Frequent Symbol": most_frequent_symbol,
        "Most Active Time": f"{most_active_time}:00",
        "Avg Trade Volume": f"{avg_trade_volume:.2f}",
        "Largest Volume Trade": f"{largest_volume_trade:.2f}",
        "Most Frequent Outcome": most_frequent_trade_outcome,
        # Market Condition
        "Best Day Profit": f"{daily_profit[best_day_profit]:.2f}" if best_day_profit else "N/A",
        "Worst Day Profit": f"{daily_profit[worst_day_profit]:.2f}" if worst_day_profit else "N/A",
        "Average Daily Profit": f"{avg_daily_profit:.2f}" if not daily_profit.empty else "N/A",
        "Best Week Profit": f"{weekly_profit[best_week_profit]:.2f}" if best_week_profit else "N/A",
        "Worst Week Profit": f"{weekly_profit[worst_week_profit]:.2f}" if worst_week_profit else "N/A",
        "Best Symbol Profit": best_symbol_profit,
        "Worst Symbol Profit": worst_symbol_profit,
        "Avg Profit By Symbol": avg_profit_by_symbol,
        "Profit Volatility By Symbol": profit_volatility_by_symbol
        }
    
    return stats

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
            # Query the database to get the `api_account_id` and `account_id` for the selected account
            account_info = get_account_info(user_id, account_selection)  # Assuming this returns (api_account_id, account_id)

            if account_info:
                api_account_id, account_id = account_info  # Unpack the account info tuple

                # Retrieve trades for the specific account
                trades = get_account_trades(api_account_id)

                # Convert the result into a DataFrame
                trades_df = pd.DataFrame(trades)
                

                if trades_df.empty:
                    st.info("No trading data available.")

                else:
                    trades_df['close_time'] = pd.to_datetime(trades_df['close_time'])
                    trades_df['cum_gain'] = trades_df['gain'].cumsum()
                    trades_df['type'] = trades_df['type'].replace({
                                            'DEAL_TYPE_SELL': 'Sell',
                                            'DEAL_TYPE_BUY': 'Buy'
                                        })

                    statistics = calculate_trade_statistics(trades_df)

                    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Performance", "Trade Journal", "Analytic Tools", "AI Insights", "Settings"])

                    with tab1: # ------ PERFORMANCE STATS ------ #
                        
                        # ------ OVERVIEW ------ #

                        st.subheader("Overview", anchor=False)
                        st.caption(f"General performance overview for account {account_selection}.")

                        chart, stats = st.columns([3, 1], vertical_alignment="bottom")

                        with chart:
                            with tile("overview_chart", 385):
                                st.markdown("**Overview**")

                                line_chart(
                                    data=trades_df, 
                                    x='close_time', 
                                    y='cum_gain', 
                                    x_label='Time', 
                                    y_label='Cumulative Gain (%)', 
                                    height=335
                                )

                        with stats:
                            metric_tile("performance_overview_stat_1", "Total Gain", statistics['Total Gain'], 40, "secondary", None)
                            metric_tile("performance_overview_stat_2", "Win Rate", statistics['Win Rate'], 40, "primary", None)
                            metric_tile("performance_overview_stat_3", "Profit Factor", statistics['Profit Factor'], 40, "primary", None)
                            metric_tile("performance_overview_stat_4", "Account Age", statistics['Account Age'], 40, "primary", None)
                            metric_tile("performance_overview_stat_5", "Most Traded Symbol", statistics['Most Traded Symbol'], 40, "primary", None)

                        st.divider()

                        # ------ TRADE EFFICIENCY ------ #
                    
                        st.subheader("Trade Efficiency", anchor=False)
                        st.caption("Evaluate the effectiveness and precision of recent trades based on set metrics.")

                        chart, stats = st.columns([3, 1], vertical_alignment="bottom")

                        with chart:
                            with tile("trade_efficiency_chart", 385):
                                st.markdown("**Chart**")

                                scatter_chart(
                                    data=trades_df, 
                                    x='duration_mins', 
                                    y='gain', 
                                    x_label='Duration (Mins)', 
                                    y_label='Gain (%)', 
                                    height=335
                                )

                        with stats:
                            metric_tile("performance_efficiency_stat_1", "Avg Trade Duration", statistics['Avg Trade Duration'], 40, "primary", None)
                            metric_tile("performance_efficiency_stat_2", "Avg Profit Per Trade", statistics['Avg Profit Per Trade'], 40, "primary", None)
                            metric_tile("performance_efficiency_stat_3", "Max Profit", statistics['Max Profit'], 40, "primary", None)
                            metric_tile("performance_efficiency_stat_4", "Min Profit", statistics['Min Profit'], 40, "primary", None)
                            metric_tile("performance_efficiency_stat_5", "Most Frequent Type", statistics['Most Frequent Type'], 40, "primary", None)

                        st.divider()

                        # ------ RISK ANALYSIS ------ #
                    
                        st.subheader("Risk Analysis", anchor=False)
                        st.caption("Assess trading risks and operational efficiency to optimize risk management strategies.")

                        chart, stats = st.columns([3, 1], vertical_alignment="bottom")

                        with chart:
                            with tile("risk_analysis_chart", 385):
                                st.markdown("**Chart**")

                        with stats:
                            metric_tile("performance_risk_stat_1", "Max Drawdown", statistics['Max Drawdown'], 40, "primary", None)
                            metric_tile("performance_risk_stat_2", "Avg Risk Per Trade", statistics['Avg Risk Per Trade'], 40, "primary", None)
                            metric_tile("performance_risk_stat_3", "Sharpe Ratio", statistics['Sharpe Ratio'], 40, "primary", None)
                            metric_tile("performance_risk_stat_4", "Risk Reward Ratio", statistics['Risk Reward Ratio'], 40, "primary", None)
                            metric_tile("performance_risk_stat_5", "Trades at Risk", statistics['Trades at Risk'], 40, "primary", None)

                        st.divider()

                        # ------ BEHAVIOURAL PATTERNS ------ #
                    
                        st.subheader("Behavioural Patterns", anchor=False)
                        st.caption("Identify trends in trading behavior that impact performance outcomes.")

                        chart, stats = st.columns([3, 1], vertical_alignment="bottom")

                        with chart:
                            with tile("behavioural_patterns_chart", 385):
                                st.markdown("**Chart**")

                        with stats:
                            metric_tile("performance_behaviour_stat_1", "Most Frequent Symbol", statistics['Most Frequent Symbol'], 40, "primary", None)
                            metric_tile("performance_behaviour_stat_2", "Most Active Time", statistics['Most Active Time'], 40, "primary", None)
                            metric_tile("performance_behaviour_stat_3", "Avg Trade Volume", statistics['Avg Trade Volume'], 40, "primary", None)
                            metric_tile("performance_behaviour_stat_4", "Largest Volume Trade", statistics['Largest Volume Trade'], 40, "primary", None)
                            metric_tile("performance_behaviour_stat_5", "Most Frequent Outcome", statistics['Most Frequent Outcome'], 40, "primary", None)

                        st.divider()

                        # ------ MARKET CONDITION ANALYSIS ------ #
                    
                        st.subheader("Market Condition Analysis", anchor=False)
                        st.caption("Analyse how different market conditions influence trade decisions and results.")

                        chart, stats = st.columns([3, 1], vertical_alignment="bottom")

                        with chart:
                            with tile("market_condition_chart", 385):
                                st.markdown("**Chart**")

                        with stats:
                            metric_tile("performance_market_stat_1", "Best Symbol Profit", statistics['Best Symbol Profit'], 40, "primary", None)
                            metric_tile("performance_market_stat_2", "Worst Symbol Profit", statistics['Worst Symbol Profit'], 40, "primary", None)
                            metric_tile("performance_market_stat_3", "Most Traded Symbol", statistics['Most Traded Symbol'], 40, "primary", None)
                            metric_tile("performance_market_stat_4", "Stat 4", "Value", 40, "primary", None)
                            metric_tile("performance_market_stat_5", "Stat 5", "Value", 40, "primary", None)

                        st.divider()

                        # ------ DAILY/WEEKLY PERFORMANCE SUMMARY ------ #
                    
                        st.subheader("Daily/Weekly Performance Summary", anchor=False)
                        st.caption("Summary of performance metrics over daily and weekly intervals for tracking progress and trends.")

                        chart, stats = st.columns([3, 1], vertical_alignment="bottom")

                        with chart:
                            with tile("daily_weekly_summary_chart", 385):
                                st.markdown("**Chart**")

                        with stats:
                            metric_tile("performance_summary_stat_1", "Best Day Profit", statistics['Best Day Profit'], 40, "primary", None)
                            metric_tile("performance_summary_stat_2", "Worst Day Profit", statistics['Worst Day Profit'], 40, "primary", None)
                            metric_tile("performance_summary_stat_3", "Average Daily Profit", statistics['Average Daily Profit'], 40, "primary", None)
                            metric_tile("performance_summary_stat_4", "Best Week Profit", statistics['Best Week Profit'], 40, "primary", None)
                            metric_tile("performance_summary_stat_5", "Worst Week Profit", statistics['Worst Week Profit'], 40, "primary", None)

                    with tab2: # ------ TRADING JOURNAL ------ #
                        st.subheader("Trading Jorunal", anchor=False)
                        st.caption(f"Journal of all trades for account {account_selection}.")

                        # Create the new DataFrame with renamed columns
                        trades_display = trades_df.rename(columns={
                            'ticket': 'Ticket',
                            'symbol': 'Symbol',
                            'type': 'Type',
                            'volume': 'Volume',
                            'open_time': 'Open Time',
                            'open_price': 'Open Price',
                            'close_time': 'Close Time',
                            'close_price': 'Close Price',
                            'profit': 'Profit',
                            'gain': 'Gain'
                        })[
                            ['Ticket', 'Symbol', 'Type', 'Volume', 'Open Time', 
                            'Open Price', 'Close Time', 'Close Price', 'Profit', 'Gain']
                        ]

                        # Add an empty Notes column if not present
                        if "Notes" not in trades_display.columns:
                            trades_display['Notes'] = ""

                        # Editable table with disabled columns for read-only data
                        edited_trades_display = st.data_editor(
                            trades_display,
                            column_config={
                                "Ticket": "Ticket",
                                "Symbol": "Symbol",
                                "Type": "Trade Type",
                                "Volume": "Volume",
                                "Open Time": "Open Time",
                                "Open Price": "Open Price",
                                "Close Time": "Close Time",
                                "Close Price": "Close Price",
                                "Profit": "Profit",
                                "Gain": "Gain",
                                "Notes": st.column_config.TextColumn(
                                    "Notes",
                                    help="Add notes for each trade",
                                    max_chars=500,
                                ),
                            },
                            disabled=["Ticket", "Symbol", "Type", "Volume", "Open Time", 
                                    "Open Price", "Close Time", "Close Price", "Profit", "Gain"],
                            hide_index=True,
                            use_container_width=True
                        )

        else:
            st.info("No Account Selected")
      
def systems_page():
    with st.container(border=False):
        gradient_text("Systems", "2em")

        # Sample data
        data = {
            "Position": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "Name": ["Jonny D", "Mathe W", "Mathe W", "Rami H", "Joseph G", "Jessikan B", "Ajit A", "Hamed T", "Jonny D", "Ali B"],
            "Account Size": ["$10,000.00", "$200,000.00", "$200,000.00", "$100,000.00", "$200,000.00", "$200,000.00", "$200,000.00", "$200,000.00", "$10,000.00", "$25,000.00"],
            "Account Gain": ["$433.80", "$10,321.75", "$8,067.62", "$3,240.85", "$5,471.17", "$5,087.50", "$4,977.00", "$4,716.26", "$166.00", "$348.39"],
            "Gain %": ["5.34%", "5.16%", "4.03%", "3.24%", "2.74%", "2.54%", "2.49%", "2.36%", "1.66%", "1.4%"],
            "Country": ["United Kingdom", "United Arab Emirates", "United Arab Emirates", "Canada", "--", "Australia", "Belgium", "--", "United Kingdom", "United Kingdom"]
        }

        # Create a DataFrame
        df = pd.DataFrame(data)

        # Custom styles for leaderboard
        st.markdown(
            """
            <style>
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 1em;
                }
                th, td {
                    border-bottom: 1px solid #ddd;
                    text-align: left;
                    padding: 8px;
                }
                th {
                    background-color: #111111;
                    color: white;
                }
                tr:nth-child(even) {
                    background-color: #111111;
                }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Display the leaderboard
        st.markdown("### Highest Growth")
        st.markdown(df.to_html(index=False, escape=False), unsafe_allow_html=True)

def settings_page():
    with st.container(border=False):
        gradient_text("Settings", "2em")

def logout_page():
    gradient_text("Logout", "2em")

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
    
    with bottom():
        social_media_links = [
            "https://x.com/blackboxstats",
            "https://www.instagram.com/blackboxstats"
        ]

        social_media_icons = SocialMediaIcons(social_media_links)

        social_media_icons.render()

pg = st.navigation(pages, position="sidebar")
pg.run()
