import streamlit as st
import altair as alt
from static.elements import tile, metric_tile, promo_container, animated_container, line_chart, column_chart
import pandas as pd
import datetime as dt
import numpy as np
from utils.stats import get_account_trades, get_user_accounts, get_account_info
from streamlit_extras.stylable_container import stylable_container

now = dt.datetime.now(dt.timezone.utc)  # Get current time in UTC
current_time = now.hour + now.minute / 60  # Convert to hour with decimal minutes

def DashboardPage():
    with st.container(border=False):
        first_name = st.session_state.get("first_name", "User")
        user_id = st.session_state.get("user_id", "User")

        # Get the list of account numbers for the user
        account_numbers = get_user_accounts(user_id)
        
        st.subheader(f"Welcome back, {first_name}!", anchor=False)
        st.caption("Explore comprehensive data on your trading activity, subscriber base, and earnings.")
    
        st.markdown("")

        col1, col2, col3, col4 = st.columns(4, vertical_alignment="bottom")

        with col1:
            animated_container(
                key="dashboard_plan_card", 
                content=f"""
                    <div style="line-height: 1.4;">
                        <p style="margin: 0; font-size: 0.75em; color: #878884;">Plan</p>
                        <p style="margin: 0; font-size: 1em; font-weight: bold; color: #E8E8E8;">Premium ✨</p>
                    </div>
                    """
                )

        with col2:
            metric_tile(
                key="dashboard_stat_1", 
                stat="Linked Accounts", 
                value="3 of 10", 
                height=40, 
                type="primary",
                border=True,
                tooltip=None
                )

        with col3:
            metric_tile(
                key="dashboard_stat_2", 
                stat="Member Since", 
                value="1st Jan 2024", 
                height=40, 
                type="primary",
                border=True,
                tooltip=None
                )

        with col4:
            metric_tile(
                key="dashboard_stat_3", 
                stat="Trader Rank", 
                value="#1340", 
                height=40, 
                type="primary",
                border=True,
                tooltip=None
                )
        
        overview_tab, systems_tab, tools_tab = st.tabs(["Overview", "Systems", "Trading Tools"])

        with overview_tab:
            with tile(
                "systems-accounts-performance-chart",
                300,
                True
            ):
                    st.markdown("**Accounts performance**")
                    
                    # Sample data for subscriber count over time
                    subscriber_data = pd.DataFrame({
                        "Date": pd.date_range(start="2024-01-01", periods=12, freq="M"),
                        "Gain (%)": [0, 2, 5, 3, 10, 12, 8, 9, 15, 25, 50, 45]
                    })

                    # Generate the chart
                    line_chart(
                        data=subscriber_data, 
                        x="Date", 
                        y="Gain (%)", 
                        x_label="Date", 
                        y_label="Gain (%)",
                        height=250,
                        show_labels=False
                        )
                
            # Sample data for systems
            accounts_data = [
                {
                    "Account No.": f"800{np.random.randint(10000, 99999)}",
                    "Net Gain (%)": round(np.random.uniform(-10, 50), 2),
                    "Performance": np.random.randn(30).cumsum(),
                    "Drawdown": -np.abs(np.random.randn(30).cumsum()),
                    "Black Box Score": np.random.randint(60, 100),
                }
                for _ in range(10)  # Generate 10 sample accounts
            ]

            # Print the data
            for account in accounts_data:
                print(account)

            # Convert data to DataFrame
            accounts_df = pd.DataFrame(accounts_data)

            # Displaying the table for systems
            st.dataframe(
                accounts_df,
                column_config={
                    "Account No.": st.column_config.TextColumn(
                        label="Account Number",
                        help="Unique identifier for the account."
                    ),
                    "Net Gain (%)": st.column_config.NumberColumn(
                        label="Net Gain (%)",
                        format="%.2f%%"
                    ),
                    "Performance": st.column_config.AreaChartColumn(
                        label="Performance",
                        y_min=accounts_df["Performance"].apply(lambda x: min(x)).min(),
                        y_max=accounts_df["Performance"].apply(lambda x: max(x)).max(),
                        help="Cumulative performance over time."
                    ),
                    "Drawdown": st.column_config.BarChartColumn(
                        label="Drawdown",
                        y_min=accounts_df["Drawdown"].apply(lambda x: min(x)).min(),
                        y_max=accounts_df["Drawdown"].apply(lambda x: max(x)).max(),
                        help="Visual representation of drawdown over time."
                    ),
                    "Black Box Score": st.column_config.ProgressColumn(
                        label="AnalytiQ Score",
                        format="%d",
                        help="Rating of the system based on historical performance and risk."
                    ),
                },
                hide_index=True,
                use_container_width=True
            )


            with tile(
                "tab-test",
                300,
                True
            ):
                subtab1, subtab2 = st.tabs(["Tab 1", "Tab 2"])

                with subtab1:
                    st.caption("Test")

        with systems_tab:

            col1, col2 = st.columns(2, vertical_alignment="bottom")

            with col1:
                with tile(
                    key="system_subscriber_chart",
                    height=300,
                    border=True
                ):
                    st.markdown("**Total Subscriber Count**")
                    
                    # Sample data for subscriber count over time
                    subscriber_data = pd.DataFrame({
                        "Date": pd.date_range(start="2024-01-01", periods=12, freq="M"),
                        "Subscribers": [0, 2, 5, 3, 10, 12, 8, 9, 15, 25, 50, 45]
                    })

                    # Generate the chart
                    line_chart(
                        data=subscriber_data, 
                        x="Date", 
                        y="Subscribers", 
                        x_label="Date", 
                        y_label="Number of Subscribers",
                        height=250,
                        show_labels=False
                        )

            with col2:
                with tile(
                    key="system_revenue_chart",
                    height=300,
                    border=True
                ):
                    st.markdown("**Subscrition Revenue**")
                    
                    # Sample data for subscriber revenue over time
                    revenue_data = pd.DataFrame({
                        "Date": pd.date_range(start="2024-01-01", periods=12, freq="M"),
                        "Revenue": [0, 100, 250, 150, 500, 600, 400, 450, 750, 950, 1000, 850]
                    })

                    # Generate the chart
                    column_chart(
                        data=revenue_data, 
                        x="Date", 
                        y="Revenue", 
                        x_label="Date", 
                        y_label="Revenue",
                        height=250,
                        show_labels=False
                        )

            # Sample data for systems
            systems_data = [
                {
                    "System Name": "System A",
                    "Net Gain (%)": round(np.random.uniform(-10, 50), 2),  # Random net gain percentage
                    "Performance": np.random.randn(30).cumsum(),
                    "Black Box Score": np.random.randint(60, 100),  # Score out of 100
                    "Subscribers": round(np.random.uniform(0, 50), 0),
                    "Revenue ($)": round(np.random.uniform(0, 15000), 2),
                },
                {
                    "System Name": "System B",
                    "Net Gain (%)": round(np.random.uniform(-10, 50), 2),
                    "Performance": np.random.randn(30).cumsum(),
                    "Black Box Score": np.random.randint(60, 100),
                    "Subscribers": round(np.random.uniform(0, 50), 0),
                    "Revenue ($)": round(np.random.uniform(0, 15000), 2),
                },
                {
                    "System Name": "System C",
                    "Net Gain (%)": round(np.random.uniform(-10, 50), 2),
                    "Performance": np.random.randn(30).cumsum(),
                    "Black Box Score": np.random.randint(60, 100),
                    "Subscribers": round(np.random.uniform(0, 50), 0),
                    "Revenue ($)": round(np.random.uniform(0, 15000), 2),
                },
                {
                    "System Name": "System D",
                    "Net Gain (%)": round(np.random.uniform(-10, 50), 2),
                    "Performance": np.random.randn(30).cumsum(),
                    "Black Box Score": np.random.randint(60, 100),
                    "Subscribers": round(np.random.uniform(0, 50), 0),
                    "Revenue ($)": round(np.random.uniform(0, 15000), 2),
                },
            ]

            # Convert data into a pandas DataFrame
            systems_df = pd.DataFrame(systems_data)

            # Displaying the table for Systems
            st.dataframe(
                systems_df,
                column_config={
                    "System Name": "Portfolio System",
                    "Net Gain (%)": st.column_config.NumberColumn(
                        "Net Gain (%)", 
                        format="%.2f%%"
                    ),
                    "Performance": st.column_config.AreaChartColumn(
                        "Performance Sparkline",
                        y_min=systems_df["Performance"].apply(lambda x: min(x)).min(),
                        y_max=systems_df["Performance"].apply(lambda x: max(x)).max(),
                    ),
                    "Black Box Score": st.column_config.ProgressColumn(
                        "Black Box Score",
                        format="%d",
                        help="The Black Box Score rates the portfolio based on historical performance and risk metrics.",
                    ),
                    "Subscribers": st.column_config.NumberColumn(
                    "Subscribers"
                    ),
                    "Revenue ($)": st.column_config.NumberColumn(
                        "Revenue ($)", 
                        format="$%.2f"
                    ),
                },

                hide_index=True, use_container_width=True
            )

if __name__ == "__main__":
    DashboardPage()
