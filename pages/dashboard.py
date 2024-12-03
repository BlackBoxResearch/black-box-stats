import streamlit as st
import altair as alt
from static.elements import tile, metric_tile, promo_container, promo_container, line_chart, column_chart
import pandas as pd
import datetime as dt
import numpy as np
from utils.stats import get_account_trades, get_user_accounts, get_account_info

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
            promo_container(
                key="dashboard_plan_card", 
                content=f"""
                    <div style="line-height: 1.44;">
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
        
        tab1, tab2, tab3 = st.tabs(["Overview", "Systems", "Trading Tools"])

        with tab1:
            
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
                
            calendar, feed = st.columns([1, 2], vertical_alignment="bottom")

            with calendar:
                with tile(
                    key="economic-calendar",
                    height=300,
                    border=True
                ):
                    st.markdown("**Economic Calendar**")
                    st.caption("""
                                00:01 UK BRC Retail Sales YoY -3.4% 0.6% 0.3%
                               
                                00:30 Australian Current Account Balance-14.1B--10.7B
                               
                                07:00 Turkish CPI YoY -46.6%48.58%
                               
                                07:00 Turkish CPI MoM -1.92%2.88%
                               
                                07:30 Swiss Core CPI YoY -0.9%0.8%
                               
                                07:30 Swiss CPI YoY -0.7%0.6%
                               
                                07:30 Swiss CPI MoM --0.1%-0.1%

                                """)

            with feed:
                with tile(
                    key="news-feed",
                    height=300,
                    border=True
                ):
                    st.markdown("**News Feed**")
                    st.caption("""
                                ICBC Financial Services avoids SEC fine for cybersecurity breach

                                23:23 Dec 02
                                    
                                Gold drops on strong US Dollar boosted by ISM improvement

                                23:15 Dec 02FXStreet
                                    
                                Williams: No Signs of Recession Detected

                                23:09 Dec 02
                                    
                                Williams: Expect More Data Before December Meeting

                                23:09 Dec 02
                                    
                                Williams: Avoiding Excessive Restrictions to Allow for Economic Growth

                                23:09 Dec 02
                                    
                                Fed's Williams Addresses Reporters Following Event in Queens, NY

                                23:09 Dec 02
                                    
                                Williams thinks monetary policy is still restrictive

                                23:09 Dec 02
                                    
                                John Williams, NY Fed President: Direction is Towards Lower Rates Over Time

                                23:09 Dec 02
                                    
                                Williams of the Federal Reserve: Key to return inflation to 2%

                                23:09 Dec 02
                                    
                                Fed's Williams says policy should remain somewhat restrictive due to inflation

                                23:09 Dec 02
                                    
                                Fed's Williams Sees No Signs of a US Recession

                                23:09 Dec 02
                                    
                                As Trump fumes over unlikely ‘Brics currency’, China should talk to US more about money

                                23:01 Dec 02South China Morning Post
                                    
                                Iraqi fighters head to Syria to battle rebels but Lebanon’s Hezbollah stays out: sources

                                23:01 Dec 02South China Morning Post
                                    
                                GBP/USD turns bearish, ends three-day winstreak

                                23:00 Dec 02FXStreet
                                    
                                South Korea Consumer Price Index Growth (MoM) below forecasts (-0.1%) in November: Actual (-0.3%)

                                23:00 Dec 02FXStreet
                                    
                                South Korea Consumer Price Index Growth (YoY) below expectations (1.7%) in November: Actual (1.5%)


                    
                                """)

        with tab2:

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

        with tab3:

            tool1, tool2 = st.columns(2, vertical_alignment="bottom")

            with tool1:
                with tile(
                    key="tool-1",
                    height=200,
                    border=True
                ):
                    st.caption("Trading Tool 1")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.button("Explore1")

            with tool2:
                with tile(
                    key="tool-2",
                    height=200,
                    border=True
                ):
                    st.caption("Trading Tool 2")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.button("Explore2")

            tool3, tool4 = st.columns(2, vertical_alignment="bottom")

            with tool3:
                with tile(
                    key="tool-3",
                    height=200,
                    border=True
                ):
                    st.caption("Trading Tool 3")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.button("Explore3")

            with tool4:
                with tile(
                    key="tool-4",
                    height=200,
                    border=True
                ):
                    st.caption("Trading Tool 4")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.button("Explore4")

            tool5, tool6 = st.columns(2, vertical_alignment="bottom")

            with tool5:
                with tile(
                    key="tool-5",
                    height=200,
                    border=True
                ):
                    st.caption("Trading Tool 5")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.button("Explore5")

            with tool6:
                with tile(
                    key="tool-6",
                    height=200,
                    border=True
                ):
                    st.caption("Trading Tool 6")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.markdown("")
                    st.button("Explore6")

if __name__ == "__main__":
    DashboardPage()
